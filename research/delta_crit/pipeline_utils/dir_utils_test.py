import os
import sys

import pytest

from research.delta_crit.pipeline_utils.dir_utils import set_up_populated_workdir


def test_set_up_populated_workdir_pass(scenario_id_garching) -> None:
    workdir = set_up_populated_workdir(example_scenario_id=scenario_id_garching)
    assert os.path.isdir(workdir)
    assert os.path.isfile(os.path.join(workdir, f"{scenario_id_garching}.xml"))
    assert os.path.isfile(os.path.join(workdir, f"{scenario_id_garching}.yaml"))


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
