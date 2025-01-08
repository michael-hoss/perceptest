import sys

import pytest

from research.delta_crit.pem.pem_config import PemConfig, Perror, pem_config_from_json


def test_load_pem_config_from_list_of_dicts(example_pem_config_list_of_dicts: list[dict]) -> None:
    pem_config: PemConfig = Perror.schema().load(example_pem_config_list_of_dicts, many=True)  # type: ignore
    assert pem_config[0].object_id == 201


def test_load_pem_config_from_file(example_pem_config_path: str) -> None:
    pem_config: PemConfig = pem_config_from_json(example_pem_config_path)
    assert isinstance(pem_config[0], Perror)
    assert pem_config[0].object_id == 201


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
