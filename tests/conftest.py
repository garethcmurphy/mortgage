
import os
import sys
import pytest

# Add the module's directory to sys.path
@pytest.fixture(scope="session", autouse=True)
def add_module_path():
    """
    Automatically adds the path to the modules to sys.path for testing.
    Modify the `module_path` below if needed to point to the correct location.
    """
    # Define the path to the module directory
    module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))

    # Add to sys.path if not already there
    if module_path not in sys.path:
        sys.path.insert(0, module_path)