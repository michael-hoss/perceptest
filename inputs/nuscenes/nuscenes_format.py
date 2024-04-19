from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, TypeAlias
from uuid import uuid4

from base.geometry.vectors import Quaternion, Vector2, Vector3

"""See https://github.com/nutonomy/nuscenes-devkit/blob/master/docs/schema_nuscenes.md for details."""


class Guid(str):
    """Custom string class for GUIDs"""

    def __new__(cls, value=None):
        if value is None:
            value = str(uuid4().hex)
        elif not cls.is_valid_guid(value):
            raise ValueError("Invalid GUID format")

        return super().__new__(cls, value)

    @classmethod
    def is_valid_guid(cls, value: str) -> bool:
        # Empty strings are allowed upon creation.
        # Convention: they will be replaced by an actual guid later on.
        # Some may stay empty if e.g. a sample has no predecessor.

        if (isinstance(value, str) and len(value) == 32) or value == "":
            return True
        return False


@dataclass
class NuScenesWritable:
    """Base class for all nuScenes classes that correspond to a json file"""

    token: Guid

    @property
    def json_filename(self) -> str:
        raise NotImplementedError("This field must be implemented by the subclass.")

    def to_dict(self) -> dict:
        raise NotImplementedError("This field must be implemented by the subclass.")


@dataclass
class Attribute(NuScenesWritable):
    """Properties for different types of objects/road users"""

    name: str = "vehicle.moving"
    description: str = "Vehicle is moving."

    json_filename: str = field(default="attribute.json")

    def to_dict(self):
        dict_representation = asdict(self)
        dict_representation.pop("json_filename")
        return dict_representation


@dataclass
class CalibratedSensor(NuScenesWritable):
    """Mounting position and potentially intrinsic calibration of one sensor"""

    sensor_token: Guid
    translation: Vector3 = field(default_factory=Vector3)
    rotation: Quaternion = field(default_factory=Quaternion)
    camera_intrinsic: list[float] = field(default_factory=list)

    json_filename: str = field(default="calibrated_sensor.json")

    def to_dict(self):
        return {
            "token": self.token,
            "sensor_token": self.sensor_token,
            "translation": self.translation,
            "rotation": self.rotation,
            "camera_intrinsic": self.camera_intrinsic,
        }


@dataclass
class Category(NuScenesWritable):
    """Object classification"""

    name: str = "vehicle.car"
    description: str = (
        "Vehicle designed primarily for personal use, e.g. sedans, hatch-backs, wagons, vans, mini-vans, "
        "SUVs and jeeps. If the vehicle is designed to carry more than 10 people use vehicle.bus. "
        "If it is primarily designed to haul cargo use vehicle.truck. "
    )

    json_filename: str = field(default="category.json")

    def to_dict(self):
        dict_representation = asdict(self)
        dict_representation.pop("json_filename")
        return dict_representation


@dataclass
class EgoPose(NuScenesWritable):
    """Ego vehicle position at one time stamp in the global frame"""

    timestamp: int  # in e-6 seconds
    rotation: Quaternion = field(default_factory=Quaternion)
    translation: Vector3 = field(default_factory=Vector3)

    json_filename: str = field(default="ego_pose.json")

    def to_dict(self):
        return {
            "token": self.token,
            "timestamp": self.timestamp,
            "rotation": self.rotation,
            "translation": self.translation,
        }


@dataclass
class Instance(NuScenesWritable):
    """One object track over time"""

    category_token: Guid
    nbr_annotations: int
    first_annotation_token: Guid  # foreign key to SampleAnnotation
    last_annotation_token: Guid  # foreign key to SampleAnnotation

    json_filename: str = field(default="instance.json")

    def to_dict(self):
        dict_representation = asdict(self)
        dict_representation.pop("json_filename")
        return dict_representation


@dataclass
class Log(NuScenesWritable):
    """Metadata of one recording session file"""

    logfile: str  #  "n015-2018-07-24-11-22-45+0800"
    vehicle: str  # "n015"
    date_captured: str  # "2018-07-24"
    location: str  # "singapore-onenorth"

    json_filename: str = field(default="log.json")

    def to_dict(self):
        dict_representation = asdict(self)
        dict_representation.pop("json_filename")
        return dict_representation


@dataclass
class Map(NuScenesWritable):
    """Metadata of one map file"""

    category: str  #  "semantic_prior"

    filename: str  # "maps/53992ee3023e5494b90c316c183be829.png"
    log_tokens: list[Guid] = field(default_factory=list)  # Logs that got recorded in this map

    json_filename: str = field(default="map.json")

    def to_dict(self):
        dict_representation = asdict(self)
        dict_representation.pop("json_filename")
        return dict_representation


@dataclass
class Sample(NuScenesWritable):
    """One keyframe in a scene.
    From docs: A sample is an annotated keyframe at 2 Hz.
    The data is collected at (approximately) the same timestamp as part of a single LIDAR sweep."""

    timestamp: int
    prev: Guid
    next: Guid
    scene_token: Guid

    json_filename: str = field(default="sample.json")

    def to_dict(self):
        dict_representation = asdict(self)
        dict_representation.pop("json_filename")
        return dict_representation


@dataclass
class SampleAnnotation(NuScenesWritable):
    """The reference annotation for one object in one frame.
    All location data is given with respect to the global coordinate system."""

    sample_token: Guid
    instance_token: Guid
    visibility_token: str
    prev: Guid  # temporally previous annotation of the same object instance
    next: Guid  # temporally next annotation of the same object instance
    num_lidar_pts: int
    num_radar_pts: int
    translation: Vector3 = field(default_factory=Vector3)  # center_x, center_y, center_z
    size: Vector3 = field(default_factory=Vector3)  # width, length, height
    rotation: Quaternion = field(default_factory=Quaternion)
    attribute_tokens: list[Guid] = field(default_factory=list)

    json_filename: str = field(default="sample_annotation.json")

    def to_dict(self):
        return {
            "token": self.token,
            "sample_token": self.sample_token,
            "instance_token": self.instance_token,
            "visibility_token": self.visibility_token,
            "prev": self.prev,
            "next": self.next,
            "num_lidar_pts": self.num_lidar_pts,
            "num_radar_pts": self.num_radar_pts,
            "translation": self.translation,
            "size": self.size,
            "rotation": self.rotation,
            "attribute_tokens": self.attribute_tokens,
        }


@dataclass
class SampleData(NuScenesWritable):
    """This is additional information to one frame in time (Sample),
    especially links to raw data like camera images or lidar point clouds"""

    sample_token: Guid
    ego_pose_token: Guid
    calibrated_sensor_token: Guid
    timestamp: int
    fileformat: str
    is_key_frame: bool
    height: int  # of camera image in pixels; 0 if not applicable
    width: int  # of camera image in pixels; 0 if not applicable
    filename: str
    prev: Guid
    next: Guid

    json_filename: str = field(default="sample_data.json")

    def to_dict(self):
        dict_representation = asdict(self)
        dict_representation.pop("json_filename")
        return dict_representation


@dataclass
class Scene(NuScenesWritable):
    """A scene is one recorded snippet, and consists of several samples/frames"""

    log_token: Guid
    nbr_samples: int  # number frames in scene
    first_sample_token: Guid
    last_sample_token: Guid
    name: str  # e.g. "scene-0001"
    description: str  # "Construction, maneuver between several trucks"

    json_filename: str = field(default="scene.json")

    def to_dict(self):
        dict_representation = asdict(self)
        dict_representation.pop("json_filename")
        return dict_representation


@dataclass
class Sensor(NuScenesWritable):
    """Metadata of one sensor"""

    channel: str  # CAM_FRONT, CAM_FRONT_RIGHT, ...
    modality: str  # camera, lidar, radar, ...

    json_filename: str = field(default="sensor.json")

    def to_dict(self):
        dict_representation = asdict(self)
        dict_representation.pop("json_filename")
        return dict_representation


@dataclass
class Visibility(NuScenesWritable):
    """Bin for an object visibility percentage range"""

    description: str  # "visibility of whole object is between 0 and 40%"
    level: str  # "v0-40"

    json_filename: str = field(default="visibility.json")

    def to_dict(self):
        dict_representation = asdict(self)
        dict_representation.pop("json_filename")
        return dict_representation


@dataclass
class Split:
    """Gives information of a dataset split.
    The usual splits like train, val, test, etc. are already handled by the nuScenes devkit.
    This class is for custom splits that one may create to test specific own sets of scenarios."""

    name: str
    scene_names: list[str]

    json_filename: str = field(default="splits.json")

    # Make class hashable to be able to easily detect duplicates
    def __eq__(self, other):
        return (
            isinstance(other, Split)
            and self.name == other.name
            and sorted(self.scene_names) == sorted(other.scene_names)
        )

    def __hash__(self):
        return hash((self.name, tuple(n for n in sorted(self.scene_names))))


def get_splits_dict(splits: list[Split]) -> dict[str, list[str]]:
    return {split.name: split.scene_names for split in splits}


@dataclass
class SampleResult:
    """Analogous to SampleAnnotation, but for the data under test."""

    # see also "Results Format" on https://www.nuscenes.org/tracking
    sample_token: Guid  # Foreign key. Identifies the sample/keyframe for which objects are detected.

    tracking_id: str  # Unique object id that is used to identify an object track across samples.

    # The predicted class for this sample_result, e.g. car, pedestrian.
    # Note that the tracking_name cannot change throughout a track.
    tracking_name: str

    # Object prediction score between 0 and 1 for the class identified by tracking_name.
    #  We average over frame level scores to compute the track level score.
    # The score is used to determine positive and negative tracks via thresholding.
    tracking_score: float

    # Estimated bounding box location center in meters in the global frame (x,y,z).
    translation: Vector3 = field(default_factory=Vector3)

    # Estimated bounding box size in meters: width, length, height.
    size: Vector3 = field(default_factory=Vector3)

    # Estimated bounding box orientation as quaternion in the global frame: w, x, y, z.
    rotation: Quaternion = field(default_factory=Quaternion)

    # Estimated bounding box velocity in m/s in the global frame: vx, vy.
    velocity: Vector2 = field(default_factory=Vector2)

    def to_dict(self):
        return {
            "sample_token": self.sample_token,
            "tracking_id": self.tracking_id,
            "tracking_name": self.tracking_name,
            "tracking_score": self.tracking_score,
            "translation": self.translation,
            "size": self.size,
            "rotation": self.rotation,
            "velocity": self.velocity,
        }


@dataclass
class TrackingSubmissionMeta:
    """Metadata of one tracking task submission"""

    # Boolean values: whether the submission uses these types of data as input
    use_camera: bool
    use_lidar: bool
    use_radar: bool
    use_map: bool
    use_external: bool  # "external" is also not further specified on https://www.nuscenes.org/tracking

    def to_dict(self):
        return asdict(self)


TrackingResults: TypeAlias = Dict[Guid, List[SampleResult]]
MetricsSummary: TypeAlias = Dict[str, Any]


def tracking_results_to_dict(results: TrackingResults) -> dict:
    tracking_results_dict = {}
    for sample_guid, sample_results in results.items():
        tracking_results_dict[sample_guid] = [sample_result.to_dict() for sample_result in sample_results]
    return tracking_results_dict


@dataclass
class TrackingSubmission(NuScenesWritable):
    meta: TrackingSubmissionMeta  # Metadata of the submission.

    # Maps each sample_token (frame) to a list of sample_results (perceived objects).
    results: TrackingResults

    json_filename: str = field(default="tracking_results.json")

    def to_dict(self):
        return {
            "meta": self.meta.to_dict(),
            "results": tracking_results_to_dict(self.results),
        }


@dataclass
class NuScenesReference:
    """Contains all information of the dataset, just as in e.g. v1.0-mini or v1.0-trainval.
    This is only the reference data / nuScenes-provided information"""

    attributes: list[Attribute]
    calibrated_sensors: list[CalibratedSensor]
    categories: list[Category]
    ego_poses: list[EgoPose]
    instances: list[Instance]
    logs: list[Log]
    maps: list[Map]
    samples: list[Sample]
    sample_annotations: list[SampleAnnotation]
    sample_data_list: list[SampleData]
    scenes: list[Scene]
    sensors: list[Sensor]
    visibility: list[Visibility]


@dataclass
class NuScenesAll:
    """Contains both the reference data and the results of the tracking task under test"""

    reference: NuScenesReference
    submission: TrackingSubmission
    splits: list[Split]


@dataclass
class TrackingEvalParams:
    """Parameters besides config for evaluation of tracking results"""

    result_path: str  # Path to the tracking results json file.
    output_dir: str  # Path to folder where the evaluation results will be saved to.
    eval_set: str  # split to evaluate on: train, val, mini_val, (test, custom_string_if_implemented)
    nusc_dataroot: str  # (Absolute) path to the  dataset folder.
    nusc_version: str  # v1.0-trainval or v1.0-mini, or custom_dir_name if data is available there
    verbose: bool = True  # Whether to print to stdout
    render_classes: Optional[list[str]] = None  # Classes to render to disk or None
