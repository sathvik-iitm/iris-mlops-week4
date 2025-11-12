#!/usr/bin/env python3
"""
Load Testing Tool for Week 7
Simulates wrk-like behavior with configurable load
"""

import requests
import time
import concurrent.futures
import statistics
from datetime import datetime
import sys

def make_request(url, request_id):
    """Make a single prediction request"""
    start = time.time()
    try:
        response = requests.post(
            f"{url}/predict",
            json={
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            },
            timeout=10
        )
        duration = time.time() - start
        return {
            'success': response.status_code == 200,
            'duration': duration,
            'status': response.status_code
        }
    except Exception as e:
        return {
            'success': False,
            'duration': time.time() - start,
            'status': 0,
            'error': str(e)
        }

def run_load_test(url, total_requests, concurrent_workers, test_name):
    """Run load test with specified parameters"""
    print(f"\n{'='*70}")
    print(f"🔥 {test_name}")
    print(f"{'='*70}")
    print(f"Target: {url}")
    print(f"Requests: {total_requests}")
    print(f"Workers: {concurrent_workers}")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*70}\n")
    
    start_time = time.time()
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_workers) as executor:
        futures = [executor.submit(make_request, url, i) for i in range(total_requests)]
        
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            completed += 1
            
            if completed % 100 == 0:
                elapsed = time.time() - start_time
                rate = completed / elapsed
                print(f"Progress: {completed}/{total_requests} ({completed/total_requests*100:.1f}%) | "
                      f"Rate: {rate:.1f} req/s")
    
    total_time = time.time() - start_time
    
    # Calculate statistics
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    if successful:
        durations = [r['duration'] * 1000 for r in successful]  # Convert to ms
        avg = statistics.mean(durations)
        p50 = statistics.median(durations)
        p95 = sorted(durations)[int(len(durations) * 0.95)]
        p99 = sorted(durations)[int(len(durations) * 0.99)]
        min_d = min(durations)
        max_d = max(durations)
    else:
        avg = p50 = p95 = p99 = min_d = max_d = 0
    
    # Print results
    print(f"\n{'='*70}")
    print(f"📊 RESULTS")
    print(f"{'='*70}")
    print(f"\n⏱️  Duration & Throughput:")
    print(f"   Total Time: {total_time:.2f}s")
    print(f"   Throughput: {total_requests/total_time:.2f} req/s")
    print(f"   Avg Response: {avg:.2f}ms")
    
    print(f"\n✅ Success Rate:")
    print(f"   Successful: {len(successful)}/{total_requests} ({len(successful)/total_requests*100:.1f}%)")
    print(f"   Failed: {len(failed)}/{total_requests} ({len(failed)/total_requests*100:.1f}%)")
    
    print(f"\n📈 Response Time Percentiles:")
    print(f"   Min: {min_d:.2f}ms")
    print(f"   P50: {p50:.2f}ms")
    print(f"   P95: {p95:.2f}ms")
    print(f"   P99: {p99:.2f}ms")
    print(f"   Max: {max_d:.2f}ms")
    
    if failed:
        print(f"\n❌ Failed Requests: {len(failed)}")
    
    print(f"{'='*70}\n")
    
    return {
        'total_time': total_time,
        'throughput': total_requests/total_time,
        'success_rate': len(successful)/total_requests * 100,
        'avg_response': avg,
        'p50': p50,
        'p95': p95,
        'p99': p99
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_test.py <URL> [requests] [workers]")
        print("Example: python load_test.py http://34.123.45.67 1000 10")
        sys.exit(1)
    
    url = sys.argv[1].rstrip('/')
    requests_count = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    run_load_test(url, requests_count, workers, "LOAD TEST")
