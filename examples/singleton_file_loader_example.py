from jinnang.common.patterns import SingletonFileLoader
from jinnang.verbosity import Verbosity



print("--- SingletonFileLoader Example ---")

# --- Demonstrate loading a file relative to the caller_module_path ---
# The loader will search for 'conf/sample_config.yml' relative to this script's location
config_loader_1 = SingletonFileLoader(
    filename="conf/sample_config.yml",
    caller_module_path=__file__,
    verbosity=Verbosity.FULL
)

print("\n--- Load Configuration (First Attempt) ---")
if config_loader_1.loaded_filepath:
    print(f"Successfully loaded config from: {config_loader_1.loaded_filepath}")
    with open(config_loader_1.loaded_filepath, 'r') as f:
        content = f.read()
    print(f"Content:\n{content}")
else:
    print(f"Failed to load config: conf/sample_config.yml")

# --- Demonstrate Singleton behavior ---
# Subsequent calls with the same parameters should return the same instance
config_loader_2 = SingletonFileLoader(
    filename="conf/sample_config.yml",
    caller_module_path=__file__,
    verbosity=Verbosity.FULL
)

print("\n--- Demonstrate Singleton Behavior (Second Attempt) ---")
print(f"Is config_loader_1 the same instance as config_loader_2? {config_loader_1 is config_loader_2}")

# --- Demonstrate attempting to load a non-existent file relative to caller_module_path ---


# Clear the singleton instance cache to ensure a fresh attempt for the non-existent file
SingletonFileLoader._instances.clear()

loader_non_existent = SingletonFileLoader(
    filename="conf/non_existent.yml",
    caller_module_path=__file__,
    verbosity=Verbosity.FULL
)

print("\n--- Attempt to Load Non-existent File ---")
if loader_non_existent.loaded_filepath:
    print(f"Unexpectedly loaded file: {loader_non_existent.loaded_filepath}")
else:
    print(f"Correctly failed to load non-existent file: conf/non_existent.yml")

print("\n--- Example Finished ---")