import json
from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Perror:
    """Single perception error: Manipulate object_id from start_timestep to end_timestep with offsets.
    The CS in which the offsets are specified is the ego vehicle coordinate system."""

    start_timestep: int  # included
    end_timestep: int  # excluded

    offset_longitudinal: float  # in meters
    offset_lateral: float  #  in meters
    offset_range: float  # in meters to target obstacle
    offset_azimuth: float  # in degrees, from longitudinal axis counterclockwise to target obstacle

    object_id: int  # CommonRoad obstacle id to which this error applies


# PemConfig contains all errors of a scenario
PemConfig = list[Perror]


def pem_config_from_json(json_path: str) -> PemConfig:
    with open(json_path, "r") as file:
        list_of_dicts: list[dict] = json.load(file)
    pem_config: list[Perror] = Perror.schema().load(list_of_dicts, many=True)  # type: ignore
    return pem_config
