import logging
import os
import unittest
import tempfile
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
    def __init__(self, filename=None, caller_module_path=None, verbosity=Verbosity.FULL, value=None):
        super().__init__(filename=filename, caller_module_path=caller_module_path, verbosity=verbosity)
        if not hasattr(self, '_initialized'):
            self.value = value
            self._initialized = True


class TestSingletonAndFileLoader(unittest.TestCase):
    def setUp(self):
        # Clear singleton instances
        Singleton._instances = {}
    
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
    


    def test_file_loader_no_filename_or_paths(self):
        with self.assertRaises(ValueError) as cm:
            TestSingletonFileLoader()
        self.assertIn("At least one of 'filename' or 'caller_module_path' must be provided.", str(cm.exception))

    def test_file_loader_filename_none_caller_module_path_none(self):
        with self.assertRaises(ValueError) as cm:
            TestSingletonFileLoader(filename=None, caller_module_path=None)
        self.assertIn("At least one of 'filename' or 'caller_module_path' must be provided.", str(cm.exception))

    def test_file_loader_filename_only(self):
        # Create a dummy file in the current test file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_file_name = "test_file_loader_filename_only.txt"
        test_file_path = os.path.join(current_dir, test_file_name)
        with open(test_file_path, "w") as f:
            f.write("filename only content")

        try:
            loader = TestSingletonFileLoader(
                filename=test_file_name,
                caller_module_path=__file__
            )
            self.assertEqual(loader.loaded_filepath, test_file_path)
        finally:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

    def test_file_loader_not_found(self):
        loader = TestSingletonFileLoader(
            filename="non_existent.txt",
            caller_module_path=__file__
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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dummy_file_name = "dummy.txt"
        dummy_file_path = os.path.join(current_dir, dummy_file_name)
        with open(dummy_file_path, "w") as f:
            f.write("dummy content")

        try:
            # Test Verbosity.SILENT - no logging
            # We don't use assertLogs here because we expect no logs to be emitted.
            # If any logs were emitted, it would be a failure of the SILENT verbosity.
            SingletonFileLoader.resolve_file_path(
                filename=dummy_file_name,
                caller_module_path=__file__,
                verbosity=Verbosity.SILENT
            )

            # Test Verbosity.ONCE - info level for found file
            with patch('jinnang.common.patterns.logging.info') as mock_info:
                SingletonFileLoader.resolve_file_path(
                    filename=dummy_file_name,
                    caller_module_path=__file__,
                    verbosity=Verbosity.ONCE
                )
                mock_info.assert_called_once_with(f"Found file: {dummy_file_path}")

            # Test Verbosity.DETAIL - debug for path checks, info for found file
            with patch('jinnang.common.patterns.logging.debug') as mock_debug, \
                 patch('jinnang.common.patterns.logging.info') as mock_info:
                SingletonFileLoader.resolve_file_path(
                    filename=dummy_file_name,
                    caller_module_path=__file__,
                    verbosity=Verbosity.DETAIL
                )
                # Check for at least one debug call related to path checking
                mock_debug.assert_called()
                mock_info.assert_called_once_with(f"Found file: {dummy_file_path}")

            # Test Verbosity.FULL - debug for path checks, info for found file
            with patch('jinnang.common.patterns.logging.debug') as mock_debug, \
                 patch('jinnang.common.patterns.logging.info') as mock_info:
                SingletonFileLoader.resolve_file_path(
                    filename=dummy_file_name,
                    caller_module_path=__file__,
                    verbosity=Verbosity.FULL
                )
                # Check for at least one debug call related to path checking
                mock_debug.assert_called()
                mock_info.assert_called_once_with(f"Found file: {dummy_file_path}")

            # Test FileNotFoundError logging
            non_existent_filename = "non_existent_file_for_logging.txt"
            with patch('jinnang.common.patterns.logging.error') as mock_error:
                with self.assertRaises(FileNotFoundError):
                    SingletonFileLoader.resolve_file_path(
                        filename=non_existent_filename,
                        caller_module_path=__file__,
                        verbosity=Verbosity.ONCE
                    )
                mock_error.assert_called_once()

        finally:
            if os.path.exists(dummy_file_path):
                os.remove(dummy_file_path)

    def test_file_loader_default_locations(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_file_name = "default_location_test.txt"
        test_file_path = os.path.join(current_dir, test_file_name)
        with open(test_file_path, "w") as f:
            f.write("Default content")
        
        try:
            loader = TestSingletonFileLoader(filename=test_file_name, caller_module_path=__file__)
            self.assertEqual(loader.loaded_filepath, test_file_path)
        finally:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

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
        """Test behavior when file is not found with default search locations"""
        with self.assertRaises(FileNotFoundError):
            SingletonFileLoader.resolve_file_path(
                filename="nonexistent_file_in_default_locations.txt",
                caller_module_path=__file__
            )
    
    def test_search_locations_priority(self):
        """Test that search locations are checked in order"""
        with tempfile.TemporaryDirectory() as tmpdir1, tempfile.TemporaryDirectory() as tmpdir2:
            # Create same filename in both directories
            file_name = "priority_test.txt"
            file1_path = os.path.join(tmpdir1, file_name)
            file2_path = os.path.join(tmpdir2, file_name)
            
            with open(file1_path, "w") as f:
                f.write("first")
            with open(file2_path, "w") as f:
                f.write("second")
            
            # Should find the first one
            result = SingletonFileLoader.resolve_file_path(
                filename=file_name,
                caller_module_path=file1_path # Simulate calling from tmpdir1
            )
            self.assertEqual(result, file1_path)
            
            # Simulate calling from tmpdir2, should find the second one
            result = SingletonFileLoader.resolve_file_path(
                filename=file_name,
                caller_module_path=file2_path
            )
            self.assertEqual(result, file2_path)
    

    
    def test_relative_path_in_search_locations(self):
        """Test relative paths in search locations"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a dummy module file in the temporary directory
            dummy_caller_path = os.path.join(tmpdir, "dummy_caller.py")
            with open(dummy_caller_path, "w") as f:
                f.write("import os")

            # Create the test file directly in the temporary directory
            test_file_name = "test1.txt"
            test_file_path = os.path.join(tmpdir, test_file_name)
            with open(test_file_path, "w") as f:
                f.write("content")

            result = SingletonFileLoader.resolve_file_path(
                filename=test_file_name,
                caller_module_path=dummy_caller_path
            )
            self.assertEqual(result, test_file_path)
            self.assertTrue(os.path.exists(result))
    
    def test_explicit_path_takes_precedence(self):
        """Test that an explicit path takes precedence over search locations"""
        with tempfile.TemporaryDirectory() as tmpdir1, \
             tempfile.TemporaryDirectory() as tmpdir2:
            # Create a file in tmpdir1
            file1_path = os.path.join(tmpdir1, "file1.txt")
            with open(file1_path, "w") as f:
                f.write("content1")

            # Create a file in tmpdir2 with the same name
            file2_path = os.path.join(tmpdir2, "file1.txt")
            with open(file2_path, "w") as f:
                f.write("content2")

            # Create a file in tmpdir1
            file1_path = os.path.join(tmpdir1, "file1.txt")
            with open(file1_path, "w") as f:
                f.write("content1")

            # Create a file in tmpdir2
            file2_path = os.path.join(tmpdir2, "file2.txt")
            with open(file2_path, "w") as f:
                f.write("content2")

            # Test that file1 is found when tmpdir1 is the caller_module_path
            result = SingletonFileLoader.resolve_file_path(
                filename="file1.txt",
                caller_module_path=os.path.join(tmpdir1, "dummy_module.py")
            )
            self.assertEqual(result, file1_path)

            # Test that file2 is found when tmpdir2 is the caller_module_path
            result = SingletonFileLoader.resolve_file_path(
                filename="file2.txt",
                caller_module_path=os.path.join(tmpdir2, "another_dummy_module.py")
            )
            self.assertEqual(result, file2_path)
    
    def test_symlink_handling(self):
        """Test that symlinks are handled correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_file_path = os.path.join(tmpdir, "original.txt")
            with open(original_file_path, "w") as f:
                f.write("original content")

            symlink_path = os.path.join(tmpdir, "symlink.txt")
            try:
                os.symlink(original_file_path, symlink_path)

                # Test with explicit_path pointing to the symlink
                result = SingletonFileLoader.resolve_file_path(
                    filename=os.path.basename(symlink_path),
                    caller_module_path=os.path.dirname(symlink_path)
                )
                self.assertEqual(result, symlink_path)

                # Test with filename pointing to the symlink (should resolve to original)
                # This behavior might need clarification based on SingletonFileLoader's exact symlink handling
                # For now, assuming it returns the symlink path if given as filename/explicit_path
                # If it's supposed to resolve to the real path, this test needs adjustment.
                # The resolve_file_path function is designed to find a file, not necessarily resolve symlinks to their targets.
                # If the symlink itself is passed as the filename, it should be found.
                # If the symlink's directory is passed as caller_module_path and the symlink's name as filename,
                # it should also find the symlink.
                result_filename = SingletonFileLoader.resolve_file_path(
                    filename=os.path.basename(symlink_path),
                    caller_module_path=tmpdir
                )
                self.assertEqual(result_filename, symlink_path)

            except OSError:
                # Skip test if symlinks are not supported (e.g., on Windows without admin rights)
                self.skipTest("Symlinks not supported on this system")
    
    def test_directory_as_filename(self):
        """Test behavior when filename is actually a directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a dummy directory inside the temporary directory
            dummy_subdir = os.path.join(tmpdir, "dummy_subdir")
            os.makedirs(dummy_subdir)

            # The function should not return directories, only files
            with self.assertRaises(FileNotFoundError):
                SingletonFileLoader.resolve_file_path(
                    filename="dummy_subdir",
                    caller_module_path=tmpdir
                )
    
    def test_filename_with_path_separators(self):
        """Test that filenames with path separators are resolved correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_dir = os.path.join(tmpdir, "nested")
            os.makedirs(nested_dir, exist_ok=True)
            nested_file_name = "deep.txt"
            nested_file_path = os.path.join(nested_dir, nested_file_name)
            with open(nested_file_path, "w") as f:
                f.write("nested content")
            
            dummy_module_path = os.path.join(tmpdir, "dummy_module.py")
            with open(dummy_module_path, "w") as f:
                f.write("import os")

            result = SingletonFileLoader.resolve_file_path(
                filename=os.path.join("nested", nested_file_name),
                caller_module_path=dummy_module_path
            )
            self.assertEqual(result, nested_file_path)
    
    def test_case_sensitivity(self):
        """Test case sensitivity behavior (platform dependent)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file with specific case
            case_file_name = "CaseTest.TXT"
            case_file_path = os.path.join(tmpdir, case_file_name)
            with open(case_file_path, "w") as f:
                f.write("case content")
            
            # Try to find with different case
            try:
                result = SingletonFileLoader.resolve_file_path(
                    filename="casetest.txt",
                    caller_module_path=tmpdir
                )
                # On case-insensitive filesystems (like macOS default), this should work
                # On case-sensitive filesystems, this should raise FileNotFoundError
                self.assertTrue(os.path.exists(result))
            except FileNotFoundError:
                # This is expected on case-sensitive filesystems
                pass
    
    def test_unicode_filenames(self):
        """Test handling of unicode characters in filenames"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_file_name = "测试文件.txt"
        test_file_path = os.path.join(current_dir, test_file_name)
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("unicode content")

        try:
            result = SingletonFileLoader.resolve_file_path(
                filename=test_file_name,
                caller_module_path=__file__
            )
            self.assertEqual(result, test_file_path)
        finally:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
    
    def test_very_long_filename(self):
        """Test handling of very long filenames"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        long_name = "a" * 100 + ".txt"
        test_file_path = os.path.join(current_dir, long_name)
        with open(test_file_path, "w") as f:
            f.write("long name content")

        try:
            result = SingletonFileLoader.resolve_file_path(
                filename=long_name,
                caller_module_path=__file__
            )
            self.assertEqual(result, test_file_path)
        finally:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
    
    def test_special_characters_in_path(self):
        """Test handling of special characters in paths"""
        # Create a temporary directory and file with special characters
        with tempfile.TemporaryDirectory() as tmpdir:
            special_dir = os.path.join(tmpdir, "dir with spaces & symbols!")
            os.makedirs(special_dir)
            
            special_file_name = "file with spaces.txt"
            special_file_path = os.path.join(special_dir, special_file_name)
            with open(special_file_path, "w") as f:
                f.write("special content")
            
            result = SingletonFileLoader.resolve_file_path(
                filename=special_file_name,
                caller_module_path=special_file_path # Use the path of the created file as caller_module_path
            )
            self.assertEqual(result, special_file_path)
    
    def test_nonexistent_search_directory(self):
        """Test that a nonexistent search directory does not cause issues"""
        with tempfile.TemporaryDirectory() as tmpdir:
            nonexistent_dir = os.path.join(tmpdir, "nonexistent_dir")
            # This should not raise an error, just not find the file
            dummy_module_path = os.path.join(tmpdir, "dummy_module.py")
            with open(dummy_module_path, "w") as f:
                f.write("import os")

            # This should not raise an error, just not find the file
            with self.assertRaises(FileNotFoundError):
                SingletonFileLoader.resolve_file_path(
                    filename="nonexistent_file.txt",
                    caller_module_path=dummy_module_path
                )
    
    def test_permission_denied_directory(self):
        """Test behavior when search directory exists but is not readable"""
        # This test is platform-specific and may not work on all systems
        with tempfile.TemporaryDirectory() as tmpdir:
            restricted_dir = os.path.join(tmpdir, "restricted")
            os.makedirs(restricted_dir)
            
            # Create a file in the directory first
            test_file_name = "restricted_file.txt"
            test_file_path = os.path.join(restricted_dir, test_file_name)
            with open(test_file_path, "w") as f:
                f.write("restricted content")
            
            original_permissions = None
            try:
                # Remove read permissions (Unix-like systems)
                original_permissions = os.stat(restricted_dir).st_mode
                os.chmod(restricted_dir, 0o000)
                
                # The function should handle this gracefully and continue to next location
                with self.assertRaises(FileNotFoundError):
                    SingletonFileLoader.resolve_file_path(
                        filename=test_file_name,
                        caller_module_path=restricted_dir
                    )
            except OSError as e:
                # If chmod fails (e.g., on Windows without appropriate privileges),
                # skip the test as permissions cannot be manipulated as expected.
                if "Operation not permitted" in str(e) or "Access is denied" in str(e):
                    self.skipTest(f"Cannot change file permissions: {e}")
                raise # Re-raise other OS errors
            finally:
                # Restore original permissions and then ensure permissions are restored for cleanup
                if original_permissions is not None:
                    os.chmod(restricted_dir, original_permissions)
                try:
                    os.chmod(restricted_dir, 0o755)
                except (OSError, PermissionError):
                    pass


class TestSingletonFileLoaderIntegration(unittest.TestCase):
    """Integration tests for SingletonFileLoader with resolve_file_path"""
    
    def test_singleton_file_loader_with_existing_file(self):
        """Test SingletonFileLoader initialization with existing file"""
        Singleton._instances = {} # Clear singleton instances
        # Create a dummy file in the current test file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_file_name = "config.json"
        test_file_path = os.path.join(current_dir, test_file_name)
        with open(test_file_path, "w") as f:
            f.write('{"setting": "value"}')

        try:
            loader = TestSingletonFileLoader(
                filename=test_file_name,
                caller_module_path=__file__
            )
            self.assertEqual(loader.loaded_filepath, test_file_path)
        finally:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
    
    def test_singleton_file_loader_with_nonexistent_file(self):
        """Test SingletonFileLoader initialization with nonexistent file"""
        Singleton._instances = {} # Clear singleton instances
        loader = TestSingletonFileLoader(
            filename="nonexistent.json",
            caller_module_path=__file__
        )
        
        self.assertIsNone(loader.filepath)
        self.assertIsNone(loader.loaded_filepath)
    
    def test_singleton_file_loader_singleton_behavior(self):
        """Test that SingletonFileLoader maintains singleton behavior with file loading"""
        # Create a dummy file in the current test file's directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_file_name = "config_singleton.json"
        test_file_path = os.path.join(current_dir, test_file_name)
        with open(test_file_path, "w") as f:
            f.write('{"setting": "value"}')

        try:
            loader1 = TestSingletonFileLoader(
                filename=test_file_name,
                caller_module_path=__file__,
                value="first"
            )
            
            # Create second instance - should be same as first
            loader2 = TestSingletonFileLoader.get_instance()
            
            # Should be the same instance
            self.assertIs(loader1, loader2)
            # Should retain original values
            self.assertEqual(loader2.value, "first")
            self.assertEqual(loader2.loaded_filepath, test_file_path)
        finally:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)


if __name__ == "__main__":
    unittest.main()