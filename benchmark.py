import time
import os
import pandas as pd
from detector import load_artifacts, predict_message


def run_benchmark(num_iterations=500):
    print("=" * 55)
    print(" AI Phishing Detector - Latency & Throughput Benchmark")
    print("=" * 55)

    print("Loading models and vectorizer...")
    start_load = time.perf_counter()
    model, vectorizer = load_artifacts()
    load_time = (time.perf_counter() - start_load) * 1000
    print(f"Artifacts loaded in: {load_time:.2f} ms")

    test_samples = [
        "Urgent: verify your bank login at http://192.168.1.1/login.php immediately!",
        "Hello, checking in regarding the team dinner tonight at 7 PM.",
        "Congratulations winner! Claim your free gift card at http://bit.ly/prize",
        "Can you send over the updated PDF for the client review?",
        "Security Alert: unauthorized password reset requested. Confirm here: http://secure-portal.xyz"
    ]

    print(f"\nBenchmarking {num_iterations} prediction requests...")
    start_bench = time.perf_counter()
    for i in range(num_iterations):
        sample = test_samples[i % len(test_samples)]
        _ = predict_message(sample, model, vectorizer)
    
    total_time = time.perf_counter() - start_bench
    avg_latency = (total_time / num_iterations) * 1000
    throughput = num_iterations / total_time

    print("\n--- Benchmark Results ---")
    print(f"Total Requests:     {num_iterations}")
    print(f"Total Time:         {total_time:.3f} s")
    print(f"Average Latency:    {avg_latency:.3f} ms / request")
    print(f"Throughput:         {throughput:.1f} requests / sec")
    print("=" * 55)


if __name__ == "__main__":
    run_benchmark()
