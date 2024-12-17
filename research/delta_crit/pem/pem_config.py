from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class PemConfig:
    """Manipulate object_id from start_timestep to end_timestep with offsets"""

    start_timestep: int
    end_timestep: int
    offset_east: float  # in meters
    offset_north: float  #  in meters
    object_id: int

    @classmethod
    def from_json_file(cls, json_path: str) -> "PemConfig":
        with open(json_path, "r") as file:
            json_string = file.read()
        pem_config: PemConfig = cls.from_json(json_string)  # type: ignore
        return pem_config
