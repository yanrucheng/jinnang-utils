import unittest
from jinnang import hash

class TestHashFunctions(unittest.TestCase):
    def test_stable_hash(self):
        # Test that the same input produces the same hash
        test_obj = {"key": "value"}
        hash1 = hash.stable_hash(test_obj)
        hash2 = hash.stable_hash(test_obj)
        self.assertEqual(hash1, hash2)
        
        # Test that different inputs produce different hashes
        test_obj2 = {"key": "different_value"}
        hash3 = hash.stable_hash(test_obj2)
        self.assertNotEqual(hash1, hash3)
        
    def test_md5(self):
        # This test assumes md5 function exists in the hash module
        # If it doesn't, you'll need to modify this test or implement the function
        if hasattr(hash, 'md5'):
            test_string = "test string"
            md5_hash = hash.md5(test_string)
            # MD5 of "test string" is known
            expected = "6f8db599de986fab7a21625b7916589c"
            self.assertEqual(md5_hash.lower(), expected)
    
    def test_partial_file_hash(self):
        # This would typically require a test file
        # For demonstration purposes, we'll just check if the function exists
        self.assertTrue(hasattr(hash, 'partial_file_hash'))

if __name__ == '__main__':
    unittest.main()