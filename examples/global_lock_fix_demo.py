#!/usr/bin/env python3
"""
Demonstration of the fix for the GlobalLockManager parameter conflict issue.

This script demonstrates the bug that was fixed where functions decorated with
@with_global_lock would fail if they had parameters named 'key' or 'timeout'.

Before the fix, this would raise:
    TypeError: GlobalLockManager.execute_sync() got multiple values for argument 'key'

After the fix, these functions work correctly.
"""

import asyncio
from jinnang.concurrency.global_lock import with_global_lock


def main():
    print("=== Global Lock Parameter Conflict Fix Demo ===")
    print()
    
    # Test 1: Function with 'key' parameter
    print("Test 1: Function with 'key' parameter")
    
    @with_global_lock("cache_operations")
    def cache_get(key, default=None):
        """Simulate a cache get operation with a 'key' parameter."""
        print(f"  Getting cache value for key: {key}")
        return f"cached_value_for_{key}" if key != "missing" else default
    
    result1 = cache_get("user_123")
    print(f"  Result: {result1}")
    print()
    
    # Test 2: Function with 'timeout' parameter
    print("Test 2: Function with 'timeout' parameter")
    
    @with_global_lock("database_operations")
    def database_query(query, timeout=30):
        """Simulate a database query with a 'timeout' parameter."""
        print(f"  Executing query: {query}")
        print(f"  With timeout: {timeout} seconds")
        return f"query_result_for_{query.replace(' ', '_')}"
    
    result2 = database_query("SELECT * FROM users", timeout=60)
    print(f"  Result: {result2}")
    print()
    
    # Test 3: Function with both 'key' and 'timeout' parameters
    print("Test 3: Function with both 'key' and 'timeout' parameters")
    
    @with_global_lock("resource_manager")
    def acquire_resource(key, timeout, resource_type="default"):
        """Simulate resource acquisition with both 'key' and 'timeout' parameters."""
        print(f"  Acquiring resource: {key}")
        print(f"  Resource type: {resource_type}")
        print(f"  Timeout: {timeout} seconds")
        return {"resource_id": key, "type": resource_type, "acquired": True}
    
    result3 = acquire_resource("gpu_0", 120, "compute_resource")
    print(f"  Result: {result3}")
    print()
    
    # Test 4: Async function with parameter conflicts
    print("Test 4: Async function with parameter conflicts")
    
    @with_global_lock("async_operations")
    async def async_process(key, timeout, data):
        """Simulate async processing with conflicting parameter names."""
        print(f"  Async processing key: {key}")
        print(f"  With timeout: {timeout}")
        print(f"  Processing data: {data}")
        await asyncio.sleep(0.1)  # Simulate async work
        return f"processed_{key}_{data}"
    
    async def run_async_test():
        result4 = await async_process("async_key", 45, "sample_data")
        print(f"  Result: {result4}")
        return result4
    
    asyncio.run(run_async_test())
    print()
    
    print("=== All tests completed successfully! ===")
    print("The parameter conflict issue has been resolved.")


if __name__ == "__main__":
    main()