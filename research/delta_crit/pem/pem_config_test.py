import os
import sys
import tempfile

import pytest

from research.delta_crit.pem.pem_config import PemConfig, Perror, pem_config_from_json, pem_config_to_json


def test_load_pem_config_from_list_of_dicts(geometrical_pem_config_list_of_dicts: list[dict]) -> None:
    pem_config: PemConfig = Perror.schema().load(geometrical_pem_config_list_of_dicts, many=True)  # type: ignore
    assert pem_config[0].object_id == 201


def test_load_pem_config_from_file(geometrical_pem_config_path: str) -> None:
    pem_config: PemConfig = pem_config_from_json(geometrical_pem_config_path)
    assert isinstance(pem_config[0], Perror)
    assert pem_config[0].object_id == 201


def test_write_pem_config_to_file(geometrical_pem_config: PemConfig) -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        json_path: str = os.path.join(temp_dir, "unittest_pem.json")
        pem_config_to_json(pem_config=geometrical_pem_config, json_path=json_path)

        assert os.path.isfile(json_path)
        written_pem_config = pem_config_from_json(json_path=json_path)
        assert written_pem_config == geometrical_pem_config


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
