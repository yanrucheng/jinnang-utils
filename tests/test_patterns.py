import os
import tempfile
import unittest
from pathlib import Path

from jinnang.common.patterns import GenericSingletonFactory


class TestSingleton(GenericSingletonFactory):
    """Test implementation of GenericSingletonFactory for testing"""
    def __init__(self, value=None):
        self.value = value


class TestGenericSingletonFactory(unittest.TestCase):
    def setUp(self):
        # Clear singleton instances before each test
        GenericSingletonFactory._instances = {}
        
        # Create temporary directory for file path tests
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
    
    def tearDown(self):
        # Clean up temporary directory
        self.temp_dir.cleanup()
    
    def test_singleton_pattern(self):
        # Test that multiple calls return the same instance
        instance1 = TestSingleton.get_instance()
        instance2 = TestSingleton.get_instance()
        self.assertIs(instance1, instance2)
        
        # Test that the instance is stored in _instances
        self.assertIn(TestSingleton, GenericSingletonFactory._instances)
        self.assertIs(GenericSingletonFactory._instances[TestSingleton], instance1)
    
    def test_singleton_with_args(self):
        # Test initialization with arguments
        instance = TestSingleton.get_instance(value="test_value")
        self.assertEqual(instance.value, "test_value")
        
        # Test that subsequent calls ignore new arguments
        instance2 = TestSingleton.get_instance(value="different_value")
        self.assertIs(instance, instance2)
        self.assertEqual(instance2.value, "test_value")  # Original value preserved
    
    def test_multiple_singleton_classes(self):
        # Define another singleton class
        class AnotherSingleton(GenericSingletonFactory):
            def __init__(self, value=None):
                self.value = value
        
        # Test that different singleton classes have different instances
        test_instance = TestSingleton.get_instance(value="test")
        another_instance = AnotherSingleton.get_instance(value="another")
        
        self.assertIsNot(test_instance, another_instance)
        self.assertEqual(test_instance.value, "test")
        self.assertEqual(another_instance.value, "another")
        
        # Verify both are in the instances dictionary
        self.assertIn(TestSingleton, GenericSingletonFactory._instances)
        self.assertIn(AnotherSingleton, GenericSingletonFactory._instances)
    
    def test_resolve_file_path_explicit_path(self):
        # Create a test file
        test_file = self.temp_path / "test_file.txt"
        with open(test_file, "w") as f:
            f.write("Test content")
        
        # Test with explicit path
        resolved_path = GenericSingletonFactory.resolve_file_path(
            explicit_path=str(test_file)
        )
        self.assertEqual(resolved_path, str(test_file))
    
    def test_resolve_file_path_search_locations(self):
        # Create subdirectories
        subdir1 = self.temp_path / "subdir1"
        subdir2 = self.temp_path / "subdir2"
        subdir1.mkdir()
        subdir2.mkdir()
        
        # Create a test file in subdir2
        test_file = subdir2 / "test_file.txt"
        with open(test_file, "w") as f:
            f.write("Test content")
        
        # Test with search locations
        search_locations = [str(subdir1), str(subdir2)]
        resolved_path = GenericSingletonFactory.resolve_file_path(
            filename="test_file.txt",
            search_locations=search_locations
        )
        self.assertEqual(resolved_path, str(test_file))
    
    def test_resolve_file_path_not_found(self):
        # Test with non-existent file
        with self.assertRaises(FileNotFoundError):
            GenericSingletonFactory.resolve_file_path(
                filename="non_existent_file.txt",
                search_locations=[str(self.temp_path)]
            )
    
    def test_resolve_file_path_caller_module_path(self):
        # Create a test file in the same directory as this test file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_file_name = "temp_test_file.txt"
        test_file_path = os.path.join(current_dir, test_file_name)
        
        try:
            # Create the test file
            with open(test_file_path, "w") as f:
                f.write("Test content")
            
            # Test with caller module path
            resolved_path = GenericSingletonFactory.resolve_file_path(
                filename=test_file_name,
                caller_module_path=__file__
            )
            self.assertEqual(resolved_path, test_file_path)
            
        finally:
            # Clean up the test file
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
    
    def test_resolve_file_path_default_locations(self):
        # Test that default locations are used when search_locations is None
        # This is more of an integration test and depends on the file structure
        
        # Create a test file in the temp directory
        test_file = self.temp_path / "test_file.txt"
        with open(test_file, "w") as f:
            f.write("Test content")
        
        # Temporarily change the current directory to the temp directory
        original_dir = os.getcwd()
        try:
            os.chdir(str(self.temp_path))
            
            # Test with default locations (should find in current directory)
            resolved_path = GenericSingletonFactory.resolve_file_path(
                filename="test_file.txt"
            )
            self.assertEqual(os.path.basename(resolved_path), "test_file.txt")
            
        finally:
            # Restore the original directory
            os.chdir(original_dir)


if __name__ == "__main__":
    unittest.main()