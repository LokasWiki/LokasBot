import unittest
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_tests():
    """Discover and run all tests in the tests directory"""
    # Initialize the test loader
    loader = unittest.TestLoader()
    
    # Discover all tests in the current directory
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Initialize a test runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run the tests
    result = runner.run(suite)
    
    # Return 0 if tests passed, 1 if tests failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 