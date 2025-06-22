import os
import tempfile
from pathlib import Path

from jinnang.common.patterns import SingletonFileLoader
from jinnang.verbosity import Verbosity

def run_example():
    print("--- SingletonFileLoader Example ---")

    # 1. Create a temporary directory and a dummy file for demonstration
    with tempfile.TemporaryDirectory() as tmpdir_name:
        temp_path = Path(tmpdir_name)
        example_file_name = "my_example_config.txt"
        example_file_content = "This is some example configuration content.\nVersion: 1.0"
        
        # Create the example file inside the temporary directory
        file_path = temp_path / example_file_name
        with open(file_path, "w") as f:
            f.write(example_file_content)
        
        print(f"Created temporary file: {file_path}")

        # 2. Demonstrate loading a file by filename and search locations
        print("\nAttempting to load file using filename and search locations...")
        # Initialize SingletonFileLoader with the filename and a list of search locations
        # The loader will search for 'my_example_config.txt' in 'temp_path'
        loader_by_filename = SingletonFileLoader(
            filename=example_file_name,
            search_locations=[str(temp_path)],
            verbosity=Verbosity.FULL # Set verbosity to see detailed logs
        )

        if loader_by_filename.loaded_filepath:
            print(f"Successfully loaded file by filename: {loader_by_filename.loaded_filepath}")
            with open(loader_by_filename.loaded_filepath, 'r') as f:
                content = f.read()
            print(f"File content:\n{content}")
        else:
            print(f"Failed to load file by filename: {example_file_name}")

        # 3. Demonstrate loading a file by explicit path
        print("\nAttempting to load file using explicit path...")
        # Initialize SingletonFileLoader with the full explicit path to the file
        loader_by_explicit_path = SingletonFileLoader(
            explicit_path=str(file_path),
            verbosity=Verbosity.FULL
        )

        if loader_by_explicit_path.loaded_filepath:
            print(f"Successfully loaded file by explicit path: {loader_by_explicit_path.loaded_filepath}")
            with open(loader_by_explicit_path.loaded_filepath, 'r') as f:
                content = f.read()
            print(f"File content:\n{content}")
        else:
            print(f"Failed to load file by explicit path: {file_path}")

        # 4. Demonstrate attempting to load a non-existent file
        print("\nAttempting to load a non-existent file...")
        non_existent_file = "non_existent_config.txt"
        
        # Clear the singleton instance cache to ensure a fresh attempt
        SingletonFileLoader._instances.clear()

        loader_non_existent = SingletonFileLoader(
            filename=non_existent_file,
            search_locations=[str(temp_path)],
            verbosity=Verbosity.FULL
        )

        if loader_non_existent.loaded_filepath:
            print(f"Unexpectedly loaded file: {loader_non_existent.loaded_filepath}")
        else:
            print(f"Correctly failed to load non-existent file: {non_existent_file}")

    print("\n--- Example Finished ---")

if __name__ == "__main__":
    run_example()