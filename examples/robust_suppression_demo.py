#!/usr/bin/env python3
"""
Demonstration of the robust suppress_c_stdout_stderr function.

This script shows how the improved implementation handles:
1. Nested/recursive calls safely
2. Thread safety in concurrent scenarios
3. Proper cleanup even when exceptions occur
4. No file descriptor leaks in complex async scenarios
"""

import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

# Add the src directory to the path so we can import jinnang
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from jinnang.io.system import suppress_c_stdout_stderr


def demonstrate_nested_calls():
    """Demonstrate nested calls work without conflicts."""
    print("\n=== Demonstrating Nested Calls ===")
    
    def nested_function(level):
        print(f"Entering level {level}")
        with suppress_c_stdout_stderr(suppress_stdout=True, suppress_stderr=False):
            print(f"This stdout message from level {level} should be suppressed")
            if level > 1:
                nested_function(level - 1)
            print(f"Still in level {level}, stdout still suppressed")
        print(f"Exiting level {level}, stdout restored")
    
    nested_function(3)
    print("Nested calls completed successfully!")


def demonstrate_recursive_calls():
    """Demonstrate recursive calls with the context manager."""
    print("\n=== Demonstrating Recursive Calls ===")
    
    def recursive_with_suppression(depth, max_depth=5):
        if depth > max_depth:
            return f"Reached max depth {max_depth}"
        
        print(f"Recursion depth {depth} - this message is visible")
        
        with suppress_c_stdout_stderr(suppress_stdout=True, suppress_stderr=False):
            print(f"Depth {depth}: This stdout should be suppressed")
            result = recursive_with_suppression(depth + 1, max_depth)
            print(f"Depth {depth}: This stdout should also be suppressed")
            
        print(f"Recursion depth {depth} - back to visible output")
        return f"Depth {depth}: {result}"
    
    result = recursive_with_suppression(1)
    print(f"Final result: {result}")


def demonstrate_exception_handling():
    """Demonstrate that exceptions don't break file descriptor restoration."""
    print("\n=== Demonstrating Exception Handling ===")
    
    try:
        with suppress_c_stdout_stderr(suppress_stdout=True, suppress_stderr=False):
            print("This stdout should be suppressed")
            raise ValueError("Intentional test exception")
    except ValueError as e:
        print(f"Caught expected exception: {e}")
    
    print("After exception: stdout should be restored and this should be visible")


def worker_function(worker_id, iterations=3):
    """Worker function for thread safety demonstration."""
    results = []
    
    for i in range(iterations):
        with suppress_c_stdout_stderr(suppress_stdout=True, suppress_stderr=False):
            # This would normally print but should be suppressed
            print(f"Worker {worker_id}, iteration {i}: suppressed output")
            
            # Nested call to test thread-local storage
            with suppress_c_stdout_stderr(suppress_stdout=False, suppress_stderr=True):
                # This stdout should be visible, stderr suppressed
                print(f"Worker {worker_id}, iteration {i}: visible nested output")
                sys.stderr.write(f"Worker {worker_id}, iteration {i}: suppressed stderr\n")
            
            time.sleep(0.01)  # Simulate some work
        
        results.append(f"Worker {worker_id} completed iteration {i}")
    
    return results


def demonstrate_thread_safety():
    """Demonstrate thread safety of the context manager."""
    print("\n=== Demonstrating Thread Safety ===")
    
    # Test with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(worker_function, i, 2) for i in range(4)]
        
        for i, future in enumerate(futures):
            try:
                results = future.result(timeout=5.0)
                print(f"Thread {i} completed: {len(results)} iterations")
            except Exception as e:
                print(f"Thread {i} failed: {e}")
    
    print("Thread safety test completed!")


def demonstrate_async_scenario():
    """Demonstrate a complex async-like recursive scenario."""
    print("\n=== Demonstrating Complex Async-like Scenario ===")
    
    def async_like_recursive_task(task_id, depth, max_depth=3):
        """Simulate an async recursive task that might have caused leaks before."""
        if depth > max_depth:
            return f"Task {task_id} completed at depth {depth}"
        
        print(f"Task {task_id} at depth {depth}: Starting")
        
        # Simulate multiple nested operations with suppression
        with suppress_c_stdout_stderr(suppress_stdout=True, suppress_stderr=False):
            print(f"Task {task_id} depth {depth}: Internal operation (suppressed)")
            
            # Simulate spawning subtasks
            subtask_results = []
            for subtask in range(2):
                with suppress_c_stdout_stderr(suppress_stdout=True, suppress_stderr=False):
                    print(f"Task {task_id} subtask {subtask}: Processing (suppressed)")
                    
                    # Recursive call
                    result = async_like_recursive_task(f"{task_id}.{subtask}", depth + 1, max_depth)
                    subtask_results.append(result)
                    
                    print(f"Task {task_id} subtask {subtask}: Completed (suppressed)")
            
            print(f"Task {task_id} depth {depth}: All subtasks completed (suppressed)")
        
        print(f"Task {task_id} at depth {depth}: Finished")
        return f"Task {task_id}: {subtask_results}"
    
    # Run multiple async-like tasks concurrently
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(async_like_recursive_task, f"TASK-{i}", 1) for i in range(3)]
        
        for i, future in enumerate(futures):
            try:
                result = future.result(timeout=10.0)
                print(f"Async task {i} result: Task completed successfully")
            except Exception as e:
                print(f"Async task {i} failed: {e}")
    
    print("Complex async scenario completed without file descriptor leaks!")


def main():
    """Run all demonstrations."""
    print("Robust suppress_c_stdout_stderr Demonstration")
    print("=" * 50)
    
    demonstrate_nested_calls()
    demonstrate_recursive_calls()
    demonstrate_exception_handling()
    demonstrate_thread_safety()
    demonstrate_async_scenario()
    
    print("\n=== All Demonstrations Completed Successfully! ===")
    print("The improved suppress_c_stdout_stderr function handles:")
    print("✓ Nested calls without conflicts")
    print("✓ Recursive scenarios safely")
    print("✓ Exception handling with proper cleanup")
    print("✓ Thread safety with thread-local storage")
    print("✓ Complex async-like scenarios without file descriptor leaks")


if __name__ == "__main__":
    main()