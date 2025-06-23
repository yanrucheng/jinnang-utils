from jinnang.common.patterns import Singleton

print("--- Singleton Example ---")

# --- Example 1: Singleton with keyword arguments ---

print("\n--- Demonstrate Singleton with keyword arguments ---")

class ConfigManager(Singleton):
    def __init__(self, config=None):
        if not hasattr(self, '_initialized'):
            print(f"ConfigManager initialized with config: {config}")
            self.config = config or {}
            self._initialized = True

# First call with keyword argument using __init__
config_manager1 = ConfigManager(config={'db': 'mysql'})
print(f"ConfigManager1 config: {config_manager1.config}")

# Second call using get_instance returns the same instance
config_manager2 = ConfigManager.get_instance()
print(f"ConfigManager2 config: {config_manager2.config}")

print(f"Is config_manager1 the same instance as config_manager2? {config_manager1 is config_manager2}")

# --- Example 2: Singleton with positional arguments ---

print("\n--- Demonstrate Singleton with positional arguments ---")

class DatabaseManager(Singleton):
    def __init__(self, db_name='default'):
        if not hasattr(self, '_initialized'):
            print(f"DatabaseManager initialized with db_name: {db_name}")
            self.db_name = db_name
            self._initialized = True

# First call with positional argument using get_instance
db_manager1 = DatabaseManager.get_instance('production_db')
print(f"DatabaseManager1 db_name: {db_manager1.db_name}")

# Second call using __init__ returns the same instance
db_manager2 = DatabaseManager()
print(f"DatabaseManager2 db_name: {db_manager2.db_name}")

print(f"Is db_manager1 the same instance as db_manager2? {db_manager1 is db_manager2}")

# --- Different Singleton classes have different instances ---
print("\n--- Demonstrate different Singleton classes have different instances ---")
print(f"Is config_manager1 the same instance as db_manager1? {config_manager1 is db_manager1}")

print("\n--- Example Finished ---")