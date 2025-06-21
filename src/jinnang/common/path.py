import functools
import platform
import time
import pytz
import cv2
import os
from datetime import datetime
from typing import TypeVar, Type, Dict, Any, Optional, List, Union

# Assuming partial_file_hash is in hash_utils
from jinnang import partial_file_hash

T = TypeVar('T')

# a decorator
def ensure_unique_path(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        original_path = func(*args, **kwargs)
        if not original_path:
            return None

        # Ensure the path is unique by appending a number if it already exists
        base, extension = os.path.splitext(original_path)
        counter = 1
        unique_path = original_path
        while os.path.exists(unique_path):
            unique_path = f"{base}-{counter}{extension}"
            counter += 1

        return unique_path
    return wrapper

class MyPath:

    def __init__(self, path):
        self.path = path

    @property
    def basename(self):
        """ Extracts the basename from a given file path. """
        return os.path.splitext(os.path.basename(self.path))[0]

    @property
    def extension(self):
        """ Extracts the extension from a given file path, without the dot. """
        return os.path.splitext(self.path)[1][1:]

    @property
    def abspath(self):
        return os.path.abspath(os.path.expanduser(self.path))

    @property
    def hash(self):
        return partial_file_hash(self.path)

    @property
    def timezone(self):
        return pytz.timezone('Asia/Shanghai')

    @property
    def timestamp(self):
        return get_file_timestamp(self.path)

    @property
    def timestr(self):
        if self.timestamp is None:
            return None
        return datetime.fromtimestamp(self.timestamp, self.timezone).strftime('%Y-%m-%d %H:%M:%S')

    @property
    def date(self):
        if self.timestamp is None:
            return None
        return datetime.fromtimestamp(self.timestamp, self.timezone).strftime('%y%m%d')

    @property
    def time_of_a_day(self):
        """
        Return a human-readable time of day for a given timestamp.
        """
        if self.timestamp is None:
            return None
        timestamp = datetime.fromtimestamp(self.timestamp, self.timezone)
        hour = timestamp.hour

        if 5 <= hour < 12:
            return 'Morning'
        elif hour == 12:
            return 'Noon'
        elif 12 < hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 21:
            return 'Evening'
        elif 21 <= hour < 24:
            return 'Night'
        else:  # from midnight to 5 am
            return 'Midnight'

@functools.lru_cache(maxsize=None)
def get_file_timestamp(path):
    timestamp = None
    try:
        stat_info = os.stat(path)
        if platform.system() == 'Windows':
            timestamp = stat_info.st_ctime
        else:
            try:
                timestamp = stat_info.st_birthtime  # macOS
            except AttributeError:
                try:
                    timestamp = stat_info.st_mtime  # Linux/Unix fallback
                except AttributeError:
                    timestamp = time.time()
    except (OSError, AttributeError):
        timestamp = time.time()
    return timestamp

def timestamp_to_date(timestamp, fstr='%y%m%d', timezone='Asia/Shanghai'):
    utc_dt = datetime.utcfromtimestamp(timestamp)
    utc_dt = utc_dt.replace(tzinfo=pytz.UTC)
    my_tz = pytz.timezone(timezone)
    my_dt = utc_dt.astimezone(my_tz)
    return my_dt.strftime(fstr)

@functools.lru_cache(maxsize=None)
def get_video_duration(file_name):
    """Extract video duration in seconds using OpenCV"""
    try:
        video = cv2.VideoCapture(file_name)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if fps > 0 and frame_count > 0:
            duration = frame_count / fps
            return duration
        return 0
    except Exception:
        return 0
    finally:
        video.release()