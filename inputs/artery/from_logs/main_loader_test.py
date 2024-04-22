import sys

import pytest

from inputs.artery.artery_format import ArterySimLog, ArterySimLogDump
from inputs.artery.from_logs.main_loader import pull_artery_sim_log


def test_main_loader(test_case_dump: ArterySimLogDump) -> None:
    artery_sim_log = pull_artery_sim_log(artery_sim_log_dump=test_case_dump)
    assert isinstance(artery_sim_log, ArterySimLog)
    # More specific tests in individual test files


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
