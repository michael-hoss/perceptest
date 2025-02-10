import hashlib
import json
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Perror:
    """Single perception error: Manipulate object_id from start_timestep to end_timestep with offsets.
    The CS in which the offsets are specified is the ego vehicle coordinate system."""

    # Set to 0 to begin from initial time step
    start_timestep: int = 0  # included

    # Set to -1 to apply until the final time step
    end_timestep: int = -1  # included!

    offset_longitudinal: float = 0  # in meters
    offset_lateral: float = 0  #  in meters
    offset_range: float = 0  # in meters to target obstacle
    offset_azimuth: float = 0  # in degrees, from longitudinal axis counterclockwise to target obstacle

    # Set to -1 to apply to all objects
    object_id: int = -1  # CommonRoad obstacle id to which this error applies


# PemConfig contains all errors of a scenario
PemConfig = list[Perror]


def pem_config_from_json(json_path: str) -> PemConfig:
    with open(json_path, "r") as file:
        list_of_dicts: list[dict] = json.load(file)
    pem_config: list[Perror] = Perror.schema().load(list_of_dicts, many=True)  # type: ignore
    return pem_config


def pem_config_to_json(pem_config: PemConfig, json_path: str) -> None:
    list_of_dicts = [perror.to_dict() for perror in pem_config]  # type: ignore
    with open(json_path, "w") as f:
        json.dump(list_of_dicts, f, indent=2)


def pem_config_from_path_or_instance(pem_config: str | PemConfig) -> PemConfig:
    if isinstance(pem_config, str):
        return pem_config_from_json(json_path=pem_config)
    elif isinstance(pem_config, list):
        for perror in pem_config:
            assert isinstance(perror, Perror)
        return pem_config
    else:
        raise ValueError("pem_config must be either path to json or PemConfig")


def int_hash_of_pem_config(pem_config: PemConfig, max_value: int = int(1e6)) -> int:
    """Compute an integer hash from a list of dataclass_json objects."""
    json_strings = [obj.to_json() for obj in pem_config]  # type: ignore
    combined_string = "|".join(json_strings)

    hash_bytes = hashlib.sha256(combined_string.encode()).digest()
    hash_int = int.from_bytes(hash_bytes, "big")
    small_int = abs(hash_int) % max_value
    return small_int
