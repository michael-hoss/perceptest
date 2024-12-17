import sys

import pytest

from research.delta_crit.pem.pem_config import PemConfig


def test_load_pem_config_from_file(example_pem_config_json: str) -> None:
    config: PemConfig = PemConfig.from_json(example_pem_config_json)  # type: ignore
    assert isinstance(config, PemConfig)
    assert config.object_id == 201


def test_load_pem_config_from_file_classmethod(example_pem_config_path: str) -> None:
    config: PemConfig = PemConfig.from_json_file(example_pem_config_path)
    assert isinstance(config, PemConfig)
    assert config.object_id == 201


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
