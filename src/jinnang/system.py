import os
import sys
import contextlib
from io import StringIO

@contextlib.contextmanager
def suppress_c_stdout_stderr(suppress_stdout=True, suppress_stderr=False):
    """A context manager that redirects C-level stdout and/or stderr to /dev/null"""
    # Flush Python-level buffers
    sys.stdout.flush()
    sys.stderr.flush()

    # Duplicate file descriptors
    old_fds = {}
    with open(os.devnull, 'wb') as fnull:
        if suppress_stdout:
            old_fds['stdout'] = os.dup(sys.stdout.fileno())
            os.dup2(fnull.fileno(), sys.stdout.fileno())

        if suppress_stderr:
            old_fds['stderr'] = os.dup(sys.stderr.fileno())
            os.dup2(fnull.fileno(), sys.stderr.fileno())

        try:
            yield
        finally:
            # Restore file descriptors
            if suppress_stdout:
                os.dup2(old_fds['stdout'], sys.stdout.fileno())
                os.close(old_fds['stdout'])

            if suppress_stderr:
                os.dup2(old_fds['stderr'], sys.stderr.fileno())
                os.close(old_fds['stderr'])

@contextlib.contextmanager
def suppress_stdout_stderr(suppress_stdout=True, suppress_stderr=False):
    """A context manager that redirects Python-level stdout and/or stderr to StringIO"""
    old_stdout, old_stderr = sys.stdout, sys.stderr
    if suppress_stdout:
        sys.stdout = StringIO()
    if suppress_stderr:
        sys.stderr = StringIO()

    try:
        yield
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr