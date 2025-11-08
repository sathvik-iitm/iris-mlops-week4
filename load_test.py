#!/usr/bin/env python3
"""
Load Testing Script for IRIS Classifier API
Simulates high traffic (1000+ requests) to test auto-scaling
"""

import requests
import time
import concurrent.futures
import statistics
from datetime import datetime

class LoadTester:
    def __init__(self, base_url, num_requests=1000, num_workers=10):
        self.base_url = base_url.rstrip('/')
        self.num_requests = num_requests
        self.num_workers = num_workers
        self.results = []
        
    def make_request(self, request_id):
        """Make a single prediction request"""
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.base_url}/predict",
                json={
                    "sepal_length": 5.1,
                    "sepal_width": 3.5,
                    "petal_length": 1.4,
                    "petal_width": 0.2
                },
                timeout=10
            )
            duration = time.time() - start_time
            return {
                'id': request_id,
                'status': response.status_code,
                'duration': duration,
                'success': response.status_code == 200
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                'id': request_id,
                'status': 0,
                'duration': duration,
                'success': False,
                'error': str(e)
            }
    
    def run_load_test(self):
        """Run the load test with concurrent workers"""
        print(f"\n{'='*70}")
        print(f"🔥 LOAD TEST STARTING")
        print(f"{'='*70}")
        print(f"Target URL: {self.base_url}")
        print(f"Total Requests: {self.num_requests}")
        print(f"Concurrent Workers: {self.num_workers}")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        
        # Run requests concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [executor.submit(self.make_request, i) for i in range(self.num_requests)]
            
            # Progress tracking
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                self.results.append(result)
                completed += 1
                
                # Print progress every 100 requests
                if completed % 100 == 0:
                    elapsed = time.time() - start_time
                    rate = completed / elapsed
                    print(f"Progress: {completed}/{self.num_requests} requests "
                          f"({completed/self.num_requests*100:.1f}%) | "
                          f"Rate: {rate:.1f} req/s")
        
        total_duration = time.time() - start_time
        self.print_results(total_duration)
    
    def print_results(self, total_duration):
        """Print test results and statistics"""
        successful = [r for r in self.results if r['success']]
        failed = [r for r in self.results if not r['success']]
        
        if successful:
            durations = [r['duration'] for r in successful]
            avg_duration = statistics.mean(durations)
            min_duration = min(durations)
            max_duration = max(durations)
            p50 = statistics.median(durations)
            p95 = sorted(durations)[int(len(durations) * 0.95)]
            p99 = sorted(durations)[int(len(durations) * 0.99)]
        else:
            avg_duration = min_duration = max_duration = p50 = p95 = p99 = 0
        
        print(f"\n{'='*70}")
        print(f"📊 LOAD TEST RESULTS")
        print(f"{'='*70}")
        print(f"\n⏱️  Duration & Throughput:")
        print(f"   Total Time: {total_duration:.2f}s")
        print(f"   Requests/sec: {self.num_requests/total_duration:.2f}")
        print(f"   Avg Request Time: {avg_duration*1000:.2f}ms")
        
        print(f"\n✅ Success Rate:")
        print(f"   Successful: {len(successful)}/{self.num_requests} "
              f"({len(successful)/self.num_requests*100:.1f}%)")
        print(f"   Failed: {len(failed)}/{self.num_requests} "
              f"({len(failed)/self.num_requests*100:.1f}%)")
        
        print(f"\n📈 Response Time Percentiles:")
        print(f"   Min: {min_duration*1000:.2f}ms")
        print(f"   P50 (median): {p50*1000:.2f}ms")
        print(f"   P95: {p95*1000:.2f}ms")
        print(f"   P99: {p99*1000:.2f}ms")
        print(f"   Max: {max_duration*1000:.2f}ms")
        
        if failed:
            print(f"\n❌ Errors:")
            error_types = {}
            for r in failed:
                error = r.get('error', 'Unknown')
                error_types[error] = error_types.get(error, 0) + 1
            for error, count in error_types.items():
                print(f"   {error}: {count}")
        
        print(f"\n{'='*70}\n")

def main():
    import sys
    
    # Default to localhost, or take URL from command line
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    num_requests = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    num_workers = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    tester = LoadTester(url, num_requests, num_workers)
    tester.run_load_test()

if __name__ == "__main__":
    main()
