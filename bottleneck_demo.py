#!/usr/bin/env python3
"""
Week 7: Bottleneck Demonstration
Shows auto-scaling and bottleneck when restricted to 1 pod
"""

import subprocess
import time
import sys

def print_section(title):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def run_kubectl_command(command, description):
    """Run kubectl command and show results"""
    print(f"🔍 {description}")
    print(f"Command: kubectl {command}")
    result = subprocess.run(
        f"kubectl {command}",
        shell=True,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print(f"Note: {result.stderr}")
    print()

def main():
    if len(sys.argv) < 2:
        print("Usage: python bottleneck_demo.py <SERVICE-IP>")
        print("Example: python bottleneck_demo.py http://34.123.45.67")
        sys.exit(1)
    
    service_url = sys.argv[1].rstrip('/')
    
    print_section("WEEK 7: AUTO-SCALING & BOTTLENECK DEMONSTRATION")
    
    print("📋 Test Plan:")
    print("   Scenario 1: Normal load (100 requests)")
    print("   Scenario 2: High load with auto-scaling (1000 requests)")
    print("   Scenario 3: Bottleneck - 1 pod restricted (1000 requests)")
    print("   Scenario 4: Bottleneck - extreme load (2000 requests)")
    print()
    
    # Initial state
    print_section("INITIAL STATE - Check HPA and Pods")
    run_kubectl_command("get hpa iris-classifier-hpa", "HPA Status")
    run_kubectl_command("get pods -l app=iris-classifier", "Current Pods")
    
    # Scenario 1: Normal Load
    input("Press ENTER to start Scenario 1 (Normal Load - 100 requests)...")
    print_section("SCENARIO 1: NORMAL LOAD (100 requests)")
    print("Expected: 1 pod, CPU <50%, no scaling\n")
    
    subprocess.run([
        'python', 'load_test.py', service_url, '100', '5'
    ])
    
    time.sleep(5)
    run_kubectl_command("get hpa iris-classifier-hpa", "HPA After Normal Load")
    run_kubectl_command("get pods -l app=iris-classifier", "Pods After Normal Load")
    
    # Scenario 2: High Load with Auto-scaling
    input("\nPress ENTER to start Scenario 2 (High Load - 1000 requests, auto-scaling enabled)...")
    print_section("SCENARIO 2: HIGH LOAD WITH AUTO-SCALING (1000 requests)")
    print("Expected: Scales from 1 → 2 → 3 pods\n")
    
    subprocess.run([
        'python', 'load_test.py', service_url, '1000', '10'
    ])
    
    print("\n⏳ Waiting 10 seconds for scaling to occur...")
    time.sleep(10)
    
    run_kubectl_command("get hpa iris-classifier-hpa", "HPA After High Load")
    run_kubectl_command("get pods -l app=iris-classifier", "Pods After Scaling")
    run_kubectl_command("top pods -l app=iris-classifier", "Pod CPU/Memory Usage")
    
    # Scenario 3: Bottleneck - Restrict to 1 pod
    input("\nPress ENTER to start Scenario 3 (Bottleneck - restrict to 1 pod)...")
    print_section("SCENARIO 3: BOTTLENECK - RESTRICTED TO 1 POD")
    print("Action: Setting HPA maxReplicas to 1 (bottleneck simulation)\n")
    
    # Scale down first
    run_kubectl_command("scale deployment iris-classifier --replicas=1", "Scale to 1 pod")
    
    # Update HPA to max 1 pod
    print("📝 Temporarily updating HPA to maxReplicas: 1")
    subprocess.run([
        'kubectl', 'patch', 'hpa', 'iris-classifier-hpa',
        '--type=json',
        '-p=[{"op": "replace", "path": "/spec/maxReplicas", "value": 1}]'
    ])
    
    time.sleep(5)
    run_kubectl_command("get hpa iris-classifier-hpa", "HPA (maxReplicas=1)")
    
    print("\n🔥 Running 1000 requests with only 1 pod allowed...")
    subprocess.run([
        'python', 'load_test.py', service_url, '1000', '10'
    ])
    
    time.sleep(5)
    run_kubectl_command("get hpa iris-classifier-hpa", "HPA Status (Bottlenecked)")
    run_kubectl_command("top pods -l app=iris-classifier", "Pod CPU (Should be very high)")
    
    # Scenario 4: Extreme bottleneck
    input("\nPress ENTER to start Scenario 4 (Extreme Bottleneck - 2000 requests, 1 pod)...")
    print_section("SCENARIO 4: EXTREME BOTTLENECK (2000 requests, 1 pod)")
    print("Expected: High failures, timeouts, degraded performance\n")
    
    subprocess.run([
        'python', 'load_test.py', service_url, '2000', '20'
    ])
    
    time.sleep(5)
    run_kubectl_command("get hpa iris-classifier-hpa", "HPA Final State")
    run_kubectl_command("top pods -l app=iris-classifier", "Final Pod Usage")
    
    # Restore HPA
    print("\n🔄 Restoring HPA to maxReplicas: 3")
    subprocess.run([
        'kubectl', 'patch', 'hpa', 'iris-classifier-hpa',
        '--type=json',
        '-p=[{"op": "replace", "path": "/spec/maxReplicas", "value": 3}]'
    ])
    
    print_section("DEMONSTRATION COMPLETE")
    print("✅ All scenarios executed!")
    print("\n📊 Key Observations:")
    print("   • Scenario 1: Single pod handles light load easily")
    print("   • Scenario 2: Auto-scaling works (1→3 pods)")
    print("   • Scenario 3: Bottleneck with 1 pod restriction")
    print("   • Scenario 4: Severe degradation at 2000 requests")
    print("\n📝 Results ready for documentation!")

if __name__ == "__main__":
    main()
