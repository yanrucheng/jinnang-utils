# Utils module

# Import submodules for easy access
from . import hash
from . import file
from . import formatting
from . import system
from . import debug
from . import arithmetic
from . import common

# Import commonly used functions and classes for direct access
from .hash import stable_hash, md5, partial_file_hash
from .file import is_bad_folder_name, is_bad_llm_caption
from .text import remove_special_chars
from .system import *
from .debug import get_python_execution_info, get_class_info, print_execution_info, print_class_info

# Import classes from the common submodule
from jinnang.common.formatters import ResolutionPreset, TruncatedPrettyPrinter, Verbosity, get_numeric
from jinnang.common.path import MyPath, ensure_unique_path, get_file_timestamp, timestamp_to_date, get_video_duration
from jinnang.common.patterns import GenericSingletonFactory
from .common import mock_when, fail_recover, custom_retry, BadInputException

# Import calculation functions
from .formatting import *
from .arithmetic import get_mode
from .geo_utils import calculate_distance_meters