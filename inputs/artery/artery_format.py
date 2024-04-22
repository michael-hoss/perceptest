from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, TypeAlias, TypedDict


class ObjectType(Enum):
    REFERENCE = 1  # object recorded by reference system
    UNDER_TEST = 2  # object recorded by object/system under test
    EGO = 3  # representation of ego vehicle


class Origin(TypedDict):
    id: int  # ground truth ID of the object
    idlocal: int  # ID of the object within the ego vehicle's tracker

    # in TAI time: https://en.wikipedia.org/wiki/International_Atomic_Time
    timestamp: int  # in e-6 seconds


class UncertainValue(TypedDict):
    value: float
    uncertainty: float


class ArteryObject(TypedDict):
    # Base class for OuT and ReS objects coming from artery logs
    # correspods to Motion_Vector_Global

    origin: Origin
    unit: str

    # Before conversion to metric:
    # long, lat, alt in WGS84 microradians, relative to globally fixed origin (even for objects under test).
    # After conversion to metric:
    # x, y, z in meters, relative to globally fixed origin.
    loc: list[UncertainValue]

    speed: UncertainValue  # in m/s. In direction of heading.

    # heading is north aligned clockwise positive,
    # but needs to be standardized to ENU (east north up) with east aligned counter-clockwise positive.
    # Heading is always relative to global coordinates.
    heading: UncertainValue  # in radians
    yaw_rate: UncertainValue  # in radians/s
    acceleration: UncertainValue  # in m/s^2. In direction of heading.
    dim: list[UncertainValue]  # in meters. Order: [width, length, height]

    # Additional/Optional fields if header is "State" instead of "Motion_Vector_Global"
    # not yet clear how orientation is specified
    orientation: UncertainValue  # in radians

    # steering can be ignored, we don't obtain it from the simulation
    steering: UncertainValue

    # parking is boolean but we don't obtain it from simulation yet
    parking: bool


@dataclass
class ArterySimLogDump:
    # Root directory of the files below
    root_dir: str

    # File names excluding the root directory
    res_file: str  # ReS = reference system
    out_file: str  # OuT = object under test
    ego_file: str  # ego vehicle


# This dict maps object ID to object frames over time
ObjectsArtery: TypeAlias = Dict[int, List[ArteryObject]]


@dataclass
class ArterySimLog:
    # Lists are values over time
    objects_out: ObjectsArtery
    objects_res: ObjectsArtery
    ego_vehicle: List[ArteryObject]
    timestamps: list[int]  # in e-6 seconds

    name: str = ""  # name of the simulation run


@dataclass
class TimeStamps:
    # This is class is just for auxiliary purposes. The ground truth of time stamps is always in the
    # actual artery data objects under ["origin"]["timestamp"].
    out: dict[int, list[int]]  # maps object ID to timestamps of its trajectory
    res: dict[int, list[int]]  # maps object ID to timestamps of its trajectory
    ego: list[int]  # timestamps of ego vehicle information
