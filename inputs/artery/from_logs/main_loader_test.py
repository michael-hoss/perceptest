import sys

import pytest

from inputs.artery.artery_format import ArteryData, FilePaths
from inputs.artery.from_logs.main_loader import pull_artery_data


def test_main_loader(test_case_paths: FilePaths) -> None:
    artery_data = pull_artery_data(file_paths=test_case_paths)
    assert isinstance(artery_data, ArteryData)
    # More specific tests in individual test files


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
