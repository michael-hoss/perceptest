import os

import debugpy
import pytest
from dotenv import load_dotenv  # type: ignore


def set_perceptest_environment_variables() -> None:
    """Since py_test targets in bazel don't inherit the ENV variables of their caller,
    we need to set the needed ENV variables here.

    This function does what `source perceptestrc.sh` does for `bazel run`.
    """

    load_dotenv(dotenv_path=".env", verbose=True)


def use_debugpy():
    """Also define this as a non-fixture function to use it in files that are not pytest tests."""

    # See also https://code.visualstudio.com/docs/python/debugging
    # To set this env var in bazel test, use --test_env=DEBUG=1
    if os.environ.get("DEBUG") == "1":
        # Make sure the IDE's debugger attaches to this port
        debugpy.listen(("localhost", 5678))
        print("Waiting for debugger to attach...")
        debugpy.wait_for_client()
        print("Debugger attached. Starting execution.")


@pytest.fixture(scope="session", autouse=True)
def always_execute():
    use_debugpy()
    set_perceptest_environment_variables()
