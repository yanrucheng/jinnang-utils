import sys
import inspect
import os
import pkgutil
from importlib.metadata import distribution

def get_python_execution_info():
    """Return information about the Python interpreter executing this script"""
    return {
        "executable_path": sys.executable,
        "version": sys.version,
        "version_info": sys.version_info,
        "platform": sys.platform
    }

def get_class_info(cls):
    """Return detailed information about a class"""
    # Get the module where the class is defined
    module = inspect.getmodule(cls)
    module_name = module.__name__ if module else "built-in"
    
    # Try to get the source file
    try:
        source_file = inspect.getsourcefile(cls) or "built-in or compiled"
    except (TypeError, OSError):
        source_file = "built-in or compiled"
    
    # Try to get the installation package
    package_info = None
    if module_name and module_name != "builtins":
        try:
            dist = distribution(module_name.split('.')[0])
            package_info = {
                "package_name": dist.metadata["Name"],
                "version": dist.version,
                "install_location": dist.locate_file('').as_posix(),
                "install_source": "pip"  # Simplification - could be conda, etc.
            }
        except:
            # If not installed via pip, try to find the file path
            try:
                if module and hasattr(module, '__file__'):
                    package_info = {
                        "package_name": module_name,
                        "install_location": os.path.dirname(module.__file__),
                        "install_source": "unknown"
                    }
            except:
                pass
    
    return {
        "class_name": cls.__name__,
        "module": module_name,
        "source_file": source_file,
        "class_dict": cls.__dict__,
        "package_info": package_info,
        "bases": [base.__name__ for base in cls.__bases__],
        "mro": [c.__name__ for c in cls.__mro__]
    }

def print_execution_info():
    """Print information about the Python interpreter"""
    info = get_python_execution_info()
    print("\nPython Execution Information:")
    print("-" * 40)
    print(f"Executable path: {info['executable_path']}")
    print(f"Version: {info['version']}")
    print(f"Platform: {info['platform']}")
    print("-" * 40)

def print_class_info(cls):
    """Print detailed information about a class"""
    info = get_class_info(cls)
    
    print(f"\nDetailed Information for Class: {info['class_name']}")
    print("-" * 60)
    print(f"Module: {info['module']}")
    print(f"Source file: {info['source_file']}")
    print(f"Bases: {', '.join(info['bases'])}")
    print(f"Method Resolution Order (MRO): {' -> '.join(info['mro'])}")
    
    if info['package_info']:
        print("\nPackage Installation Info:")
        print(f"  Package name: {info['package_info'].get('package_name', 'N/A')}")
        print(f"  Version: {info['package_info'].get('version', 'N/A')}")
        print(f"  Install location: {info['package_info'].get('install_location', 'N/A')}")
        print(f"  Install source: {info['package_info'].get('install_source', 'N/A')}")
    else:
        print("\nPackage Installation Info: Not available (may be built-in or local)")
    
    print("\nClass __dict__ Contents:")
    print("-" * 40)
    for key, value in info['class_dict'].items():
        print(f"{key}: {type(value).__name__}")
    
    print("-" * 60)