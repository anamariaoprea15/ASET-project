from Tools import Tools
import numpy as np
import threading
import psutil
import time
import logging
import concurrent.futures
import matplotlib.pyplot as plt

# Configure the logging system
logging.basicConfig(filename='monitoring.log', level=logging.DEBUG)

execution_times = []
lock = threading.Lock()

tools = Tools(4, 8, 2, [0, 1, 0, 1, 1, 0, 1, 0])

# Function to perform stress testing and collect statistics
def stress_test_generate_random_permutation(tools, iterations, matrix_size):
    execution_times = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Execute the generate_random_permutation method concurrently
        futures = [executor.submit(tools.generate_random_permutation, matrix_size) for _ in range(iterations)]

        # Wait for all futures to complete
        concurrent.futures.wait(futures)

        # Collect execution times
        for future in futures:
            try:
                result = future.result()
                # If the method returns a result, you can collect execution times
                if result is not None:
                    execution_times.append(result)  
            except Exception as e:
                print(f"Exception in stress test: {e}")

    return execution_times

def perform_resource_intensive_operation():
    try:
        # Replace this with the operation you want to test
        result = tools.generate_random_permutation(4)
    except Exception as e:
        logging.error(f"Resource utilization test: {e}")

def performance_test_generate_random_permutation(tools, n_values):
    execution_times = []

    # Ensure n_values is a list
    if not isinstance(n_values, list):
        n_values = [n_values]

    for n in n_values:
        start_time = time.time()
        try:
            # Call the method for performance testing
            result = tools.generate_random_permutation(n)
            end_time = time.time()
            execution_time = end_time - start_time
            execution_times.append(execution_time)
            logging.info(f"Performance Test: generate_random_permutation({n}) executed in {execution_time:.4f} seconds")

        except Exception as e:
            logging.exception(f"Performance Test: Exception in generate_random_permutation({n}): {e}")

    return execution_times

def monitor_resource_utilization(test_function, *args):
    before_resources = psutil.virtual_memory()
    before_cpu_percent = psutil.cpu_percent(interval=0.1)

    try:
        # Call the test function
        test_function(*args)
    except Exception as e:
        logging.error(f"Resource Utilization Test: Exception in {test_function.__name__}: {e}")
    finally:
        after_resources = psutil.virtual_memory()
        after_cpu_percent = psutil.cpu_percent(interval=0.1)

        memory_utilization_kb = max(0, after_resources.used - before_resources.used) / 1024
        cpu_utilization = max(0, after_cpu_percent - before_cpu_percent)

        logging.info(f"Resource Utilization Test: {test_function.__name__} - CPU Utilization: {cpu_utilization:.2f}%, Memory Utilization: {memory_utilization_kb:.2f} KB")
        print(f"Resource Utilization Test: {test_function.__name__} - CPU Utilization: {cpu_utilization:.2f}%, Memory Utilization: {memory_utilization_kb:.2f} KB")

    return resource_utilization

def performance_test_with_threads(tools, n_values, num_threads):
    thread_execution_times = []

    for n in n_values:
        # Clear the execution_times list before each performance test
        global execution_times
        execution_times = []

        # Simulate concurrent execution using threads
        threads = []

        for i in range(num_threads):
            # Pass 'tools', 'i', 'n', and 'lock' as arguments to perform_concurrent_operation
            thread = threading.Thread(target=perform_concurrent_operation, args=(tools, i, n, lock))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete (this line should be outside the loop above)
        for thread in threads:
            thread.join()

        avg_execution_time = sum(execution_times) / len(execution_times)
        thread_execution_times.append(avg_execution_time)

    return thread_execution_times

# Function to perform concurrent operation
def perform_concurrent_operation(tools, thread_id, n, lock):
    global execution_times  # Access the global execution_times list

    start_time = time.time()
    try:
        # Replace this with the operation you want to test
        result = tools.generate_random_permutation(n)
    except Exception as e:
        print(f"Thread {thread_id} failed with exception: {e}")
    finally:
        with lock:
            end_time = time.time()
            execution_time = end_time - start_time
            execution_times.append(execution_time)

# Define the parameters for performance testing
performance_test_n_values = [100, 500, 1000]  # Adjust as needed
num_threads_values = [5, 25, 100]  # Adjust as needed

# Perform performance testing with varying numbers of threads
for num_threads in num_threads_values:
    thread_execution_times = performance_test_with_threads(tools, performance_test_n_values, num_threads)

    # Plot the graph
    plt.plot(performance_test_n_values, thread_execution_times, label=f'{num_threads} Threads')

# Add labels and legend to the plot
plt.xlabel('Matrix Size (n)')
plt.ylabel('Average Execution Time (seconds)')
plt.legend(title='Number of Threads')
plt.title('Performance with Varying Number of Threads')

# Stress test the generate_random_permutation method with 10,000 concurrent executions
stress_test_iterations = 100000
matrix_size = 10
stress_test_execution_times = stress_test_generate_random_permutation(tools, stress_test_iterations, matrix_size)

# Convert NumPy arrays to lists for statistics.mean
stress_test_execution_times = [item.flatten().tolist() for sublist in stress_test_execution_times for item in sublist]

# Use numpy.mean instead of statistics.mean
if stress_test_execution_times:
    avg_execution_time = np.mean(stress_test_execution_times)
    min_execution_time = np.min(stress_test_execution_times)
    max_execution_time = np.max(stress_test_execution_times)

    print("Stress Test Statistics:")
    print(f"Average Execution Time: {avg_execution_time:.4f} seconds")
    print(f"Minimum Execution Time: {min_execution_time:.4f} seconds")
    print(f"Maximum Execution Time: {max_execution_time:.4f} seconds")
else:
    print("No valid results from stress test.")

# Monitor resource usage while performing the operation
before_resources = psutil.virtual_memory()
perform_resource_intensive_operation()
after_resources = psutil.virtual_memory()

# Calculate and print resource utilization metrics
resource_utilization = abs(after_resources.percent - before_resources.percent)
print(f"Resource Utilization: {resource_utilization:.2f}%")

print("\n" + "=" * 40 + "\n")

# Simulate concurrent execution using threads
concurrent_test_threads = 5
threads = []
execution_times = []

for i in range(concurrent_test_threads):
    thread = threading.Thread(target=perform_concurrent_operation, args=(tools, i, 100, lock))  # Adjust '100' as needed
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Calculate and print statistics
if execution_times:
    avg_execution_time = sum(execution_times) / len(execution_times)
    min_execution_time = min(execution_times)
    max_execution_time = max(execution_times)

    print("Concurrency Test Statistics:")
    print(f"Average Execution Time: {avg_execution_time:.6f} seconds")
    print(f"Minimum Execution Time: {min_execution_time:.6f} seconds")
    print(f"Maximum Execution Time: {max_execution_time:.6f} seconds")
else:
    print("No valid results from concurrency test.")

print("\n" + "=" * 40 + "\n")

# Performance Test: generate_random_permutation
performance_test_n_values = [100, 500, 1000]  # Adjust as needed
performance_test_execution_times = performance_test_generate_random_permutation(tools, performance_test_n_values)
for n, execution_time in zip(performance_test_n_values, performance_test_execution_times):
    print(f"Performance Test: generate_random_permutation(n={n}) executed in {execution_time:.6f} seconds")


# Resource Utilization Test: generate_random_permutation
monitor_resource_utilization(performance_test_generate_random_permutation, tools, 50)  # Adjust the value of 'n'

# Show the plot
plt.show()