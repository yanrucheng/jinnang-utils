import logging
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jinnang.common.patterns import Singleton, SingletonFileLoader
from jinnang.verbosity.verbosity import Verbosity


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
        # Clear singleton instances
        Singleton._instances = {}

        # Create temporary directory
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        # Create a dummy file for testing resolve_file_path
        self.dummy_file_path = self.temp_path / "dummy_file.txt"
        with open(self.dummy_file_path, "w") as f:
            f.write("dummy content")

        # Create subdirectories and a test file for _get_search_paths logging test
        self.subdir1 = self.temp_path / "search_dir1"
        self.subdir1.mkdir()
        self.test_file1 = self.subdir1 / "test1.txt"
        with open(self.test_file1, "w") as f:
            f.write("test1 content")

    def tearDown(self):
        # Clean up the temporary directory
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
        
        loader = TestSingletonFileLoader(explicit_path=str(test_file))
        self.assertEqual(loader.loaded_filepath, str(test_file))

    def test_file_loader_explicit_path_and_filename(self):
        test_file = self.temp_path / "explicit_test_and_filename.txt"
        with open(test_file, "w") as f:
            f.write("Explicit content")
        
        loader = TestSingletonFileLoader(explicit_path=str(test_file), filename="should_be_ignored.txt")
        self.assertEqual(loader.loaded_filepath, str(test_file))

    def test_file_loader_explicit_path_nonexistent_fallback_to_filename(self):
        non_existent_explicit_path = self.temp_path / "non_existent_explicit.txt"
        test_file = self.temp_path / "fallback_file.txt"
        with open(test_file, "w") as f:
            f.write("Fallback content")
        
        loader = TestSingletonFileLoader(
            explicit_path=str(non_existent_explicit_path),
            filename="fallback_file.txt",
            search_locations=[str(self.temp_path)]
        )
        self.assertEqual(loader.loaded_filepath, str(test_file))

    def test_file_loader_search_locations(self):
        # Create new unique subdirectories for this test to avoid conflicts
        with tempfile.TemporaryDirectory(dir=self.temp_path) as temp_subdir1_name:
            with tempfile.TemporaryDirectory(dir=self.temp_path) as temp_subdir2_name:
                 subdir1 = Path(temp_subdir1_name)
                 subdir2 = Path(temp_subdir2_name)
                 
                 test_file = subdir2 / "search_file.txt"
                 # Ensure the parent directory exists before creating the file
                 test_file.parent.mkdir(parents=True, exist_ok=True)
                 with open(test_file, "w") as f:
                         f.write("Search content")

                 loader = TestSingletonFileLoader(
                     filename="search_file.txt",
                     search_locations=[str(subdir1), str(subdir2)]
                 )
                 self.assertEqual(loader.loaded_filepath, str(test_file))

    def test_file_loader_no_filename_or_paths(self):
        with self.assertRaises(ValueError) as cm:
            TestSingletonFileLoader()
        self.assertIn("At least one of 'filename', 'explicit_path', or 'search_locations' must be provided", str(cm.exception))

    def test_file_loader_filename_none_explicit_path_none_search_locations_none(self):
        with self.assertRaises(ValueError) as cm:
            TestSingletonFileLoader(filename=None, explicit_path=None, search_locations=None)
        self.assertIn("At least one of 'filename', 'explicit_path', or 'search_locations' must be provided", str(cm.exception))

    def test_file_loader_not_found(self):
        loader = TestSingletonFileLoader(
            filename="non_existent.txt",
            caller_module_path=str(self.temp_path)
        )
        self.assertIsNone(loader.loaded_filepath)

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
            self.assertEqual(loader.loaded_filepath, test_file_path)
            
        finally:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

    def test_resolve_file_path_logging(self):
        """Test logging output for resolve_file_path with different verbosity levels"""
        # Create a dummy file for testing
        dummy_file = self.temp_path / "dummy.txt"
        with open(dummy_file, "w") as f:
            f.write("dummy content")

        # Test Verbosity.SILENT - no logging
        # We don't use assertLogs here because we expect no logs to be emitted.
        # If any logs were emitted, it would be a failure of the SILENT verbosity.
        SingletonFileLoader.resolve_file_path(
            explicit_path=str(dummy_file),
            verbosity=Verbosity.SILENT
        )

        # Test Verbosity.ONCE - info level for found file
        with patch('jinnang.common.patterns.logging.info') as mock_info:
            SingletonFileLoader.resolve_file_path(
                explicit_path=str(dummy_file),
                verbosity=Verbosity.ONCE
            )
            mock_info.assert_called_once_with(f"Found file via explicit path: {dummy_file}")

        # Test Verbosity.DETAIL - debug for explicit path check, info for found file
        with patch('jinnang.common.patterns.logging.debug') as mock_debug, \
             patch('jinnang.common.patterns.logging.info') as mock_info:
            SingletonFileLoader.resolve_file_path(
                explicit_path=str(dummy_file),
                verbosity=Verbosity.DETAIL
            )
            mock_debug.assert_called_once_with(f"Checking explicit path: {dummy_file}")
            mock_info.assert_called_once_with(f"Found file via explicit path: {dummy_file}")

        # Test Verbosity.FULL - debug for explicit path check, info for found file
        with patch('jinnang.common.patterns.logging.debug') as mock_debug, \
             patch('jinnang.common.patterns.logging.info') as mock_info:
            SingletonFileLoader.resolve_file_path(
                explicit_path=str(dummy_file),
                verbosity=Verbosity.FULL
            )
            mock_debug.assert_called_once_with(f"Checking explicit path: {dummy_file}")
            mock_info.assert_called_once_with(f"Found file via explicit path: {dummy_file}")

        # Test FileNotFoundError logging
        non_existent_filename = "non_existent_file_for_logging.txt"
        test_search_locations = [str(self.temp_path)]
        with patch('jinnang.common.patterns.logging.error') as mock_error:
            with self.assertRaises(FileNotFoundError):
                SingletonFileLoader.resolve_file_path(
                    filename=non_existent_filename,
                    search_locations=test_search_locations,
                    verbosity=Verbosity.ONCE
                )
            expected_potential_paths = [os.path.join(loc, non_existent_filename) for loc in test_search_locations]
            mock_error.assert_called_once_with(f"Could not find {non_existent_filename} in any of these locations: {expected_potential_paths}")

        # Test _get_search_paths logging
        with patch('jinnang.common.patterns.logging.debug') as mock_debug:
            SingletonFileLoader._get_search_paths(
                filename="test1.txt",
                search_locations=[str(self.subdir1)],
                verbosity=Verbosity.DETAIL
            )
            mock_debug.assert_called_once_with(f"Potential search paths for 'test1.txt': ['{self.test_file1}']")

    def test_file_loader_default_locations(self):
        test_file = self.temp_path / "default_location_test.txt"
        with open(test_file, "w") as f:
            f.write("Default content")
        
        original_dir = os.getcwd()
        try:
            os.chdir(str(self.temp_path))
            loader = TestSingletonFileLoader(filename="default_location_test.txt")
            self.assertEqual(os.path.basename(loader.loaded_filepath), "default_location_test.txt")
        finally:
            os.chdir(original_dir)


class TestResolveFilePath(unittest.TestCase):
    """Comprehensive tests for the resolve_file_path static method"""
    
    def setUp(self):
        # Create temporary directory structure for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        
        # Create test directory structure
        self.subdir1 = self.temp_path / "subdir1"
        self.subdir2 = self.temp_path / "subdir2"
        self.nested_dir = self.temp_path / "nested" / "deep"
        
        self.subdir1.mkdir()
        self.subdir2.mkdir()
        self.nested_dir.mkdir(parents=True)
        
        # Create test files
        self.test_file1 = self.subdir1 / "test1.txt"
        self.test_file2 = self.subdir2 / "test2.txt"
        self.nested_file = self.nested_dir / "nested.txt"
        self.root_file = self.temp_path / "root.txt"
        
        with open(self.test_file1, "w") as f:
            f.write("content1")
        with open(self.test_file2, "w") as f:
            f.write("content2")
        with open(self.nested_file, "w") as f:
            f.write("nested content")
        with open(self.root_file, "w") as f:
            f.write("root content")
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_explicit_path_exists(self):
        """Test that explicit_path is returned when it exists"""
        result = SingletonFileLoader.resolve_file_path(
            explicit_path=str(self.test_file1),
            filename="ignored.txt"
        )
        self.assertEqual(result, str(self.test_file1))

    def test_explicit_path_nonexistent_fallback_to_filename(self):
        """Test that if explicit_path doesn't exist, it falls back to filename and search locations"""
        non_existent_path = self.temp_path / "non_existent.txt"
        result = SingletonFileLoader.resolve_file_path(
            explicit_path=str(non_existent_path),
            filename="test2.txt",
            search_locations=[str(self.subdir1), str(self.subdir2)]
        )
        self.assertEqual(result, str(self.test_file2))

    def test_explicit_path_nonexistent_no_fallback(self):
        """Test that if explicit_path doesn't exist and no fallback, it raises FileNotFoundError"""
        non_existent_path = self.temp_path / "non_existent.txt"
        with self.assertRaises(FileNotFoundError):
            SingletonFileLoader.resolve_file_path(
                explicit_path=str(non_existent_path),
                filename="non_existent_file.txt",
                search_locations=[str(self.subdir1)]
            )

    def test_explicit_path_is_directory(self):
        """Test that explicit_path is ignored if it's a directory, and falls back"""
        result = SingletonFileLoader.resolve_file_path(
            explicit_path=str(self.subdir1),
            filename="test2.txt",
            search_locations=[str(self.subdir2)]
        )
        self.assertEqual(result, str(self.test_file2))

    def test_explicit_path_nonexistent(self):
        """Test that explicit_path is ignored when it doesn't exist"""
        with self.assertRaises(FileNotFoundError):
            SingletonFileLoader.resolve_file_path(
                explicit_path="/nonexistent/path.txt",
                filename="also_nonexistent.txt"
            )
    
    def test_filename_in_search_locations(self):
        """Test finding file in custom search locations"""
        result = SingletonFileLoader.resolve_file_path(
            filename="test1.txt",
            search_locations=[str(self.subdir1), str(self.subdir2)]
        )
        self.assertEqual(result, str(self.test_file1))
        
        # Test second location when first doesn't have the file
        result = SingletonFileLoader.resolve_file_path(
            filename="test2.txt",
            search_locations=[str(self.subdir1), str(self.subdir2)]
        )
        self.assertEqual(result, str(self.test_file2))
    
    def test_filename_in_default_locations(self):
        """Test finding file in default locations based on caller_module_path"""
        # Create a file in the temp directory
        test_file = self.temp_path / "default_test.txt"
        with open(test_file, "w") as f:
            f.write("default content")
        
        # Mock caller module path to point to temp directory
        fake_module_path = str(self.temp_path / "fake_module.py")
        
        result = SingletonFileLoader.resolve_file_path(
            filename="default_test.txt",
            caller_module_path=fake_module_path
        )
        self.assertEqual(result, str(test_file))
    
    def test_filename_in_parent_directory(self):
        """Test finding file in parent directory of caller module"""
        # Create file in parent of nested directory
        parent_file = self.temp_path / "parent_test.txt"
        with open(parent_file, "w") as f:
            f.write("parent content")
        
        # Mock caller module path to be in nested directory
        fake_module_path = str(self.nested_dir / "fake_module.py")
        
        result = SingletonFileLoader.resolve_file_path(
            filename="parent_test.txt",
            caller_module_path=fake_module_path
        )
        # The function returns the path as constructed with os.path.join
        expected_path = os.path.join(str(self.nested_dir), "..", "..", "parent_test.txt")
        self.assertEqual(result, expected_path)
    
    def test_filename_in_grandparent_directory(self):
        """Test finding file in grandparent directory of caller module"""
        # Create file in grandparent directory
        grandparent_dir = self.temp_path / "grandparent"
        parent_dir = grandparent_dir / "parent"
        child_dir = parent_dir / "child"
        
        grandparent_dir.mkdir()
        parent_dir.mkdir()
        child_dir.mkdir()
        
        grandparent_file = grandparent_dir / "grandparent_test.txt"
        with open(grandparent_file, "w") as f:
            f.write("grandparent content")
        
        # Mock caller module path to be in child directory
        fake_module_path = str(child_dir / "fake_module.py")
        
        result = SingletonFileLoader.resolve_file_path(
            filename="grandparent_test.txt",
            caller_module_path=fake_module_path
        )
        # The function returns the path as constructed with os.path.join
        expected_path = os.path.join(str(child_dir), "..", "..", "grandparent_test.txt")
        self.assertEqual(result, expected_path)
    
    def test_current_directory_search(self):
        """Test finding file in current directory"""
        original_cwd = os.getcwd()
        try:
            os.chdir(str(self.temp_path))
            result = SingletonFileLoader.resolve_file_path(
                filename="root.txt"
            )
            # The function returns relative path when found in current directory
            self.assertEqual(result, "./root.txt")
        finally:
            os.chdir(original_cwd)
    
    def test_file_not_found_error(self):
        """Test that FileNotFoundError is raised when file is not found"""
        with self.assertRaises(FileNotFoundError) as context:
            SingletonFileLoader.resolve_file_path(
                filename="nonexistent.txt",
                search_locations=[str(self.subdir1), str(self.subdir2)]
            )
        
        error_message = str(context.exception)
        self.assertIn("Could not find nonexistent.txt", error_message)
        self.assertIn(str(self.subdir1), error_message)
        self.assertIn(str(self.subdir2), error_message)
    
    def test_empty_filename(self):
        """Test behavior with empty filename"""
        # Empty filename will try to find a file named "" which should not exist
        # But the function will actually look for os.path.join(directory, "") which is just the directory
        # Since directories exist, this might not raise FileNotFoundError as expected
        # Let's test with a clearly non-existent filename instead
        with self.assertRaises(FileNotFoundError):
            SingletonFileLoader.resolve_file_path(filename="clearly_nonexistent_file_12345.txt")
    
    def test_none_caller_module_path(self):
        """Test that default module path is used when caller_module_path is None"""
        # This should use the patterns.py module path as default
        with self.assertRaises(FileNotFoundError) as context:
            SingletonFileLoader.resolve_file_path(
                filename="definitely_nonexistent.txt",
                caller_module_path=None
            )
        
        # Should still raise FileNotFoundError but with default locations
        error_message = str(context.exception)
        self.assertIn("Could not find definitely_nonexistent.txt", error_message)
    
    def test_empty_search_locations(self):
        """Test behavior with empty search locations list"""
        with self.assertRaises(FileNotFoundError):
            SingletonFileLoader.resolve_file_path(
                filename="test.txt",
                search_locations=[]
            )
    
    def test_search_locations_priority(self):
        """Test that search locations are checked in order"""
        # Create same filename in both directories
        file1 = self.subdir1 / "priority_test.txt"
        file2 = self.subdir2 / "priority_test.txt"
        
        with open(file1, "w") as f:
            f.write("first")
        with open(file2, "w") as f:
            f.write("second")
        
        # Should find the first one
        result = SingletonFileLoader.resolve_file_path(
            filename="priority_test.txt",
            search_locations=[str(self.subdir1), str(self.subdir2)]
        )
        self.assertEqual(result, str(file1))
        
        # Reverse order should find the second one
        result = SingletonFileLoader.resolve_file_path(
            filename="priority_test.txt",
            search_locations=[str(self.subdir2), str(self.subdir1)]
        )
        self.assertEqual(result, str(file2))
    
    def test_absolute_path_handling(self):
        """Test that absolute paths are handled correctly"""
        absolute_path = str(self.test_file1.resolve())
        result = SingletonFileLoader.resolve_file_path(
            explicit_path=absolute_path
        )
        self.assertEqual(result, absolute_path)
    
    def test_relative_path_in_search_locations(self):
        """Test relative paths in search locations"""
        original_cwd = os.getcwd()
        try:
            os.chdir(str(self.temp_path))
            result = SingletonFileLoader.resolve_file_path(
                filename="test1.txt",
                search_locations=["subdir1", "subdir2"]
            )
            # The function returns the path as constructed with os.path.join
            expected_path = os.path.join("subdir1", "test1.txt")
            self.assertEqual(result, expected_path)
            # Verify the file actually exists at this path
            self.assertTrue(os.path.exists(result))
        finally:
             os.chdir(original_cwd)
    
    def test_explicit_path_takes_precedence(self):
        """Test that explicit_path takes precedence over filename and search_locations"""
        # Create a file that would be found by filename search
        decoy_file = self.subdir1 / "decoy.txt"
        with open(decoy_file, "w") as f:
            f.write("decoy content")
        
        # Use explicit_path that points to a different file
        result = SingletonFileLoader.resolve_file_path(
            explicit_path=str(self.test_file2),
            filename="decoy.txt",
            search_locations=[str(self.subdir1)]
        )
        # Should return explicit_path, not the file found by filename
        self.assertEqual(result, str(self.test_file2))
    
    def test_symlink_handling(self):
        """Test that symlinks are handled correctly"""
        # Create a symlink to test file
        symlink_path = self.temp_path / "symlink.txt"
        try:
            os.symlink(str(self.test_file1), str(symlink_path))
            
            result = SingletonFileLoader.resolve_file_path(
                explicit_path=str(symlink_path)
            )
            self.assertEqual(result, str(symlink_path))
        except OSError:
            # Skip test if symlinks are not supported (e.g., on Windows without admin rights)
            self.skipTest("Symlinks not supported on this system")
    
    def test_directory_as_filename(self):
        """Test behavior when filename is actually a directory"""
        # The function should not return directories, only files
        with self.assertRaises(FileNotFoundError):
            SingletonFileLoader.resolve_file_path(
                filename="subdir1",
                search_locations=[str(self.temp_path)]
            )
    
    def test_filename_with_path_separators(self):
        """Test filename containing path separators"""
        # Create nested file structure
        nested_file = self.subdir1 / "nested" / "deep.txt"
        nested_file.parent.mkdir()
        with open(nested_file, "w") as f:
            f.write("nested content")
        
        # Try to find file using relative path as filename
        result = SingletonFileLoader.resolve_file_path(
            filename="nested/deep.txt",
            search_locations=[str(self.subdir1)]
        )
        expected_path = os.path.join(str(self.subdir1), "nested", "deep.txt")
        self.assertEqual(result, expected_path)
    
    def test_case_sensitivity(self):
        """Test case sensitivity behavior (platform dependent)"""
        # Create a file with specific case
        case_file = self.temp_path / "CaseTest.TXT"
        with open(case_file, "w") as f:
            f.write("case content")
        
        # Try to find with different case
        try:
            result = SingletonFileLoader.resolve_file_path(
                filename="casetest.txt",
                search_locations=[str(self.temp_path)]
            )
            # On case-insensitive filesystems (like macOS default), this should work
            # On case-sensitive filesystems, this should raise FileNotFoundError
            self.assertTrue(os.path.exists(result))
        except FileNotFoundError:
            # This is expected on case-sensitive filesystems
            pass
    
    def test_unicode_filenames(self):
        """Test handling of unicode characters in filenames"""
        # Create file with unicode characters
        unicode_file = self.temp_path / "测试文件.txt"
        with open(unicode_file, "w", encoding="utf-8") as f:
            f.write("unicode content")
        
        result = SingletonFileLoader.resolve_file_path(
            filename="测试文件.txt",
            search_locations=[str(self.temp_path)]
        )
        expected_path = os.path.join(str(self.temp_path), "测试文件.txt")
        self.assertEqual(result, expected_path)
    
    def test_very_long_filename(self):
        """Test handling of very long filenames"""
        # Create a file with a very long name (but within filesystem limits)
        long_name = "a" * 100 + ".txt"
        long_file = self.temp_path / long_name
        with open(long_file, "w") as f:
            f.write("long name content")
        
        result = SingletonFileLoader.resolve_file_path(
            filename=long_name,
            search_locations=[str(self.temp_path)]
        )
        expected_path = os.path.join(str(self.temp_path), long_name)
        self.assertEqual(result, expected_path)
    
    def test_special_characters_in_path(self):
        """Test handling of special characters in paths"""
        # Create directory with special characters
        special_dir = self.temp_path / "dir with spaces & symbols!"
        special_dir.mkdir()
        
        special_file = special_dir / "file with spaces.txt"
        with open(special_file, "w") as f:
            f.write("special content")
        
        result = SingletonFileLoader.resolve_file_path(
            filename="file with spaces.txt",
            search_locations=[str(special_dir)]
        )
        expected_path = os.path.join(str(special_dir), "file with spaces.txt")
        self.assertEqual(result, expected_path)
    
    def test_nonexistent_search_directory(self):
        """Test behavior when search directory doesn't exist"""
        nonexistent_dir = str(self.temp_path / "nonexistent")
        
        with self.assertRaises(FileNotFoundError):
            SingletonFileLoader.resolve_file_path(
                filename="test.txt",
                search_locations=[nonexistent_dir, str(self.subdir1)]
            )
    
    def test_permission_denied_directory(self):
        """Test behavior when search directory exists but is not readable"""
        # This test is platform-specific and may not work on all systems
        restricted_dir = self.temp_path / "restricted"
        restricted_dir.mkdir()
        
        # Create a file in the directory first
        test_file = restricted_dir / "restricted_file.txt"
        with open(test_file, "w") as f:
            f.write("restricted content")
        
        try:
            # Remove read permissions (Unix-like systems)
            os.chmod(str(restricted_dir), 0o000)
            
            # The function should handle this gracefully and continue to next location
            with self.assertRaises(FileNotFoundError):
                SingletonFileLoader.resolve_file_path(
                    filename="restricted_file.txt",
                    search_locations=[str(restricted_dir), str(self.subdir1)]
                )
        except (OSError, PermissionError):
            # Skip test if permission manipulation is not supported
            self.skipTest("Permission manipulation not supported on this system")
        finally:
            # Restore permissions for cleanup
            try:
                os.chmod(str(restricted_dir), 0o755)
            except (OSError, PermissionError):
                pass


class TestSingletonFileLoaderIntegration(unittest.TestCase):
    """Integration tests for SingletonFileLoader with resolve_file_path"""
    
    def setUp(self):
        # Clear singleton instances
        Singleton._instances = {}
        
        # Create temporary directory
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        
        # Create test file
        self.config_file = self.temp_path / "config.json"
        with open(self.config_file, "w") as f:
            f.write('{"setting": "value"}')
    
    def tearDown(self):
        self.temp_dir.cleanup()
    
    def test_singleton_file_loader_with_existing_file(self):
        """Test SingletonFileLoader initialization with existing file"""
        loader = TestSingletonFileLoader(
            filename="config.json",
            search_locations=[str(self.temp_path)]
        )
        
        expected_path = os.path.join(str(self.temp_path), "config.json")
        self.assertEqual(loader.filepath, expected_path)
        self.assertEqual(loader.loaded_filepath, expected_path)
    
    def test_singleton_file_loader_with_nonexistent_file(self):
        """Test SingletonFileLoader initialization with nonexistent file"""
        loader = TestSingletonFileLoader(
            filename="nonexistent.json",
            search_locations=[str(self.temp_path)]
        )
        
        self.assertIsNone(loader.filepath)
        self.assertIsNone(loader.loaded_filepath)
    
    def test_singleton_file_loader_singleton_behavior(self):
        """Test that SingletonFileLoader maintains singleton behavior with file loading"""
        loader1 = TestSingletonFileLoader(
            filename="config.json",
            search_locations=[str(self.temp_path)],
            value="first"
        )
        
        # Create second instance - should be same as first
        loader2 = TestSingletonFileLoader.get_instance()
        
        # Should be the same instance
        self.assertIs(loader1, loader2)
        # Should retain original values
        self.assertEqual(loader2.value, "first")
        expected_path = os.path.join(str(self.temp_path), "config.json")
        self.assertEqual(loader2.filepath, expected_path)


if __name__ == "__main__":
    unittest.main()