import os
import sys
from contextlib import contextmanager


@contextmanager
def suppress_output(stdout: bool = True, stderr: bool = True):
    # Save original stdout and stderr
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # Redirect stdout and stderr to devnull if specified
    with open(os.devnull, "w") as devnull:
        sys.stdout = devnull if stdout else original_stdout
        sys.stderr = devnull if stderr else original_stderr
        yield

    # Restore original stdout and stderr
    sys.stdout = original_stdout
    sys.stderr = original_stderr
