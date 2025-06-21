import os
import tempfile
import unittest
from pathlib import Path

from jinnang.common.patterns import Singleton, SingletonFileLoader


class TestSingleton(Singleton):
    """Test implementation of Singleton for testing"""
    def __init__(self, value=None):
        if not hasattr(self, '_initialized'):
            self.value = value
            self._initialized = True


class TestSingletonFileLoader(SingletonFileLoader):
    """Test implementation of SingletonFileLoader for testing"""
    def __init__(self, *args, value=None, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, '_initialized'):
            self.value = value
            self._initialized = True


class TestSingletonAndFileLoader(unittest.TestCase):
    def setUp(self):
        # Clear singleton instances before each test
        Singleton._instances = {}
        
        # Create temporary directory for file path tests
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
    
    def tearDown(self):
        # Clean up temporary directory
        self.temp_dir.cleanup()
    
    def test_singleton_pattern(self):
        # Test that multiple calls return the same instance
        instance1 = TestSingleton()
        instance2 = TestSingleton.get_instance()
        instance3 = TestSingleton()
        self.assertIs(instance1, instance2)
        self.assertIs(instance1, instance3)
        
        # Test that the instance is stored in _instances
        self.assertIn(TestSingleton, Singleton._instances)
        self.assertIs(Singleton._instances[TestSingleton], instance1)
    
    def test_singleton_with_args(self):
        # Test initialization with arguments
        instance = TestSingleton(value="test_value")
        self.assertEqual(instance.value, "test_value")
        
        # Test that subsequent calls ignore new arguments
        instance2 = TestSingleton(value="different_value")
        self.assertIs(instance, instance2)
        self.assertEqual(instance2.value, "test_value")  # Original value preserved

        instance3 = TestSingleton.get_instance(value="another_value")
        self.assertIs(instance, instance3)
        self.assertEqual(instance3.value, "test_value")
    
    def test_multiple_singleton_classes(self):
        # Define another singleton class
        class AnotherSingleton(Singleton):
            def __init__(self, value=None):
                if not hasattr(self, '_initialized'):
                    self.value = value
                    self._initialized = True
        
        # Test that different singleton classes have different instances
        test_instance = TestSingleton(value="test")
        another_instance = AnotherSingleton(value="another")
        
        self.assertIsNot(test_instance, another_instance)
        self.assertEqual(test_instance.value, "test")
        self.assertEqual(another_instance.value, "another")
        
        # Verify both are in the instances dictionary
        self.assertIn(TestSingleton, Singleton._instances)
        self.assertIn(AnotherSingleton, Singleton._instances)
    
    def test_file_loader_explicit_path(self):
        test_file = self.temp_path / "explicit_test.txt"
        with open(test_file, "w") as f:
            f.write("Explicit content")
        
        loader = TestSingletonFileLoader(filename=str(test_file))
        self.assertEqual(loader.loaded_filename, str(test_file))

    def test_file_loader_search_locations(self):
        subdir1 = self.temp_path / "search_dir1"
        subdir2 = self.temp_path / "search_dir2"
        subdir1.mkdir()
        subdir2.mkdir()
        
        test_file = subdir2 / "search_file.txt"
        with open(test_file, "w") as f:
            f.write("Search content")
        
        loader = TestSingletonFileLoader(
            filename="search_file.txt",
            search_locations=[str(subdir1), str(subdir2)]
        )
        self.assertEqual(loader.loaded_filename, str(test_file))

    def test_file_loader_not_found(self):
        loader = TestSingletonFileLoader(
            filename="non_existent.txt",
            caller_module_path=str(self.temp_path)
        )
        self.assertIsNone(loader.loaded_filename)

    def test_file_loader_caller_module_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_file_name = "caller_module_test.txt"
        test_file_path = os.path.join(current_dir, test_file_name)
        
        try:
            with open(test_file_path, "w") as f:
                f.write("Caller module content")
            
            loader = TestSingletonFileLoader(
                filename=test_file_name,
                caller_module_path=__file__
            )
            self.assertEqual(loader.loaded_filename, test_file_path)
            
        finally:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

    def test_file_loader_default_locations(self):
        test_file = self.temp_path / "default_location_test.txt"
        with open(test_file, "w") as f:
            f.write("Default content")
        
        original_dir = os.getcwd()
        try:
            os.chdir(str(self.temp_path))
            loader = TestSingletonFileLoader(filename="default_location_test.txt")
            self.assertEqual(os.path.basename(loader.loaded_filename), "default_location_test.txt")
        finally:
            os.chdir(original_dir)


if __name__ == "__main__":
    unittest.main()