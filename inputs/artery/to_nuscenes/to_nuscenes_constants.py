from base.geometry.vectors import Quaternion, Vector3
from inputs.nuscenes.nuscenes_format import (
    Attribute,
    CalibratedSensor,
    Category,
    Guid,
    Sensor,
    TrackingSubmissionMeta,
    Visibility,
)


class ArteryConstants:
    """Those nuScenes fields that are equal across all artery logs.

    This singleton class just serves as a namespace for constants.
    If this class had multiple instances, the randomly generated guids would not be unique anymore
    and the connections between the documents would become a mess."""

    _instance: "ArteryConstants" = None  # type: ignore

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ArteryConstants, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        # REFERENCE DATA / PROVIDED DATASET
        self.attribute_vehicle_moving = Attribute(token=Guid(), name="vehicle.moving", description="Vehicle is moving.")
        self.attribute_vehicle_stopped = Attribute(
            token=Guid(),
            name="vehicle.stopped",
            description="Vehicle, with a driver/rider in/on it, is currently stationary but has an intent to move.",
        )
        self.attribute_vehicle_parked = Attribute(
            token=Guid(),
            name="vehicle.parked",
            description="Vehicle is stationary (usually for longer duration) with no immediate intent to move.",
        )
        self.attributes = [self.attribute_vehicle_moving, self.attribute_vehicle_stopped, self.attribute_vehicle_parked]

        # We need to use this sensor for some things in the nuscenes-devkit to work, which are hard-coded to LIDAR_TOP.
        self.sensor_lidar_top = Sensor(token=Guid(), channel="LIDAR_TOP", modality="lidar")
        self.calibrated_sensor_lidar_top = CalibratedSensor(
            token=Guid(),
            sensor_token=self.sensor_lidar_top.token,
            translation=Vector3([0, 0, 0]),  # assume this sensor is in the ego frame origin
            rotation=Quaternion([1, 0, 0, 0]),  # assume this sensor just looks forward
        )

        self.category_car: Category = Category(
            token=Guid(),
            name="vehicle.car",
            description="Vehicle designed primarily for personal use, e.g. sedans, hatch-backs, wagons, vans, "
            "mini-vans, SUVs and jeeps. If the vehicle is designed to carry more than 10 people use vehicle.bus. "
            "If it is primarily designed to haul cargo use vehicle.truck. ",
        )

        self.log_vehicle = "simulated artery vehicle"
        self.log_date_captured = "not applicable"
        self.log_location = "sumo-artery-location"

        self.map_guid = Guid()  # unique guid of the one map we are using so far
        self.map_filename = "white_map.png"
        self.map_category = "semantic_prior"

        self.visibility_full = Visibility(token=Guid("1" * 32), description="fully visible (100%)", level="v100")
        self.visibility_rest = Visibility(
            token=Guid("2" * 32), description="not fully visible (0% to 99%)", level="v0-99"
        )
        self.visibility = [self.visibility_full, self.visibility_rest]

        default_vehicle_length = 4.5
        default_vehicle_width = 2.0
        default_vehicle_height = 1.5
        self.default_size = Vector3(value=[default_vehicle_length, default_vehicle_width, default_vehicle_height])

        # Default to 1 point to enable evaluation, as annotation with 0 points might be excluded from evaluation.
        self.default_num_points_annotation = 1

        # DATA UNDER TEST / SUBMISSION
        self.default_tracking_score = 1.0  # all objects are seen with full confidence
        self.default_trackig_name = "car"  # all objects are cars
        self.tracking_submission_meta = TrackingSubmissionMeta(
            use_camera=False, use_radar=False, use_lidar=False, use_map=False, use_external=True
        )

        # ORGANIZATION
        self.nuscenes_eval_config_path = "inputs/artery/to_nuscenes/artery_config_for_nuscenes.json"
