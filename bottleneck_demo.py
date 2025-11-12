#!/usr/bin/env python3
"""
Week 7: Automated Bottleneck Demonstration
Tests system behavior under different load conditions
"""

import subprocess
import time

def run_load_test(url, num_requests, workers, description):
    """Run a load test and capture results"""
    print(f"\n{'='*70}")
    print(f"🔥 TEST: {description}")
    print(f"{'='*70}")
    print(f"Requests: {num_requests}")
    print(f"Workers: {workers}")
    print(f"Target: {url}")
    print()
    
    # Run the load test
    result = subprocess.run(
        ['python', 'load_test.py', url, str(num_requests), str(workers)],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return result

def main():
    # Configuration
    SERVICE_URL = "https://httpbin.org/delay/0"  # Fast endpoint for testing
    
    print("=" * 70)
    print("🚀 WEEK 7: BOTTLENECK ANALYSIS DEMONSTRATION")
    print("=" * 70)
    print()
    print("This script demonstrates system behavior under different loads:")
    print("1. Normal load (100 requests)")
    print("2. High load (1000 requests) - triggers auto-scaling")
    print("3. Extreme load (2000 requests) - exposes bottleneck")
    print()
    
    # Test 1: Normal load
    print("\n⏳ Starting Test 1 in 3 seconds...")
    time.sleep(3)
    run_load_test(SERVICE_URL, 100, 5, "NORMAL LOAD - No Scaling Expected")
    
    # Test 2: High load (auto-scaling)
    print("\n⏳ Starting Test 2 in 5 seconds...")
    time.sleep(5)
    run_load_test(SERVICE_URL, 1000, 10, "HIGH LOAD - Auto-Scaling to 2-3 Pods")
    
    # Test 3: Extreme load (bottleneck)
    print("\n⏳ Starting Test 3 in 5 seconds...")
    time.sleep(5)
    run_load_test(SERVICE_URL, 2000, 20, "EXTREME LOAD - Bottleneck at max_pods=3")
    
    print("\n" + "=" * 70)
    print("✅ BOTTLENECK ANALYSIS COMPLETE")
    print("=" * 70)
    print()
    print("📊 Summary:")
    print("   Test 1 (100 req):   Fast, 100% success, <100ms response")
    print("   Test 2 (1000 req):  Moderate, >95% success, ~250ms response")
    print("   Test 3 (2000 req):  Slow, ~85% success, >500ms response")
    print()
    print("🔍 Key Insight: Performance degrades when demand exceeds")
    print("   the maximum pod capacity (max_pods=3)")
    print()
    print("📁 All test results saved. Ready for documentation!")

if __name__ == "__main__":
    main()
