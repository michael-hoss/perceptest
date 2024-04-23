import json
import os
import shutil
from math import cos, fabs, sin
from typing import Optional, Sequence

from PIL import Image

from base.geometry.vectors import Quaternion, Vector2, Vector3
from inputs.artery.artery_format import ArteryObject, ArterySimLog
from inputs.artery.to_nuscenes.to_nuscenes_constants import ArteryConstants
from inputs.nuscenes.nuscenes_format import (
    EgoPose,
    Guid,
    Instance,
    Log,
    Map,
    NuScenesAll,
    NuScenesReference,
    NuScenesWritable,
    Sample,
    SampleAnnotation,
    SampleData,
    SampleResult,
    Scene,
    Split,
    TrackingResults,
    TrackingSubmission,
    get_splits_dict,
)

ARTERY_CONSTANTS = ArteryConstants()


def convert_to_nuscenes_classes(artery_sim_log: ArterySimLog, nuscenes_version_dirname: str) -> NuScenesAll:
    nuscenes_reference: NuScenesReference = get_nuscenes_reference(
        artery_sim_log=artery_sim_log, nuscenes_version_dirname=nuscenes_version_dirname
    )
    nuscenes_submission: TrackingSubmission = get_nuscenes_submission(
        artery_sim_log=artery_sim_log, samples=nuscenes_reference.samples
    )
    nuscenes_splits: list[Split] = get_nuscenes_splits(nuscenes_reference=nuscenes_reference)

    nuscenes_all = NuScenesAll(reference=nuscenes_reference, submission=nuscenes_submission, splits=nuscenes_splits)
    return nuscenes_all


def get_nuscenes_splits(nuscenes_reference: NuScenesReference) -> list[Split]:
    """Create a split for all scenes and one split for each individual scene, respectively."""
    splits: list[Split] = []
    all_scene_names: list[str] = [scene.name for scene in nuscenes_reference.scenes]
    splits.append(Split(name="all", scene_names=all_scene_names))
    for scene_name in all_scene_names:
        splits.append(Split(name=scene_name, scene_names=[scene_name]))
    return splits


def get_nuscenes_reference(artery_sim_log: ArterySimLog, nuscenes_version_dirname: str) -> NuScenesReference:
    artery_log = get_log(logfile_name=artery_sim_log.name)
    artery_map = get_map(
        nuscenes_version_dirname=nuscenes_version_dirname, log_tokens=[artery_log.token], png_bytes=artery_sim_log.map
    )

    ego_poses = get_ego_poses(artery_sim_log=artery_sim_log)
    samples, scenes = get_samples_and_scenes(artery_sim_log=artery_sim_log, log_token=artery_log.token)

    sample_annotations, sample_data_list, instances = get_objects_and_frames(
        artery_sim_log=artery_sim_log, samples=samples, ego_poses=ego_poses
    )

    nuscenes_reference = NuScenesReference(
        attributes=ARTERY_CONSTANTS.attributes,
        calibrated_sensors=[ARTERY_CONSTANTS.calibrated_sensor_lidar_top],
        categories=[ARTERY_CONSTANTS.category_car],
        ego_poses=ego_poses,
        instances=instances,
        logs=[artery_log],
        maps=[artery_map],
        samples=samples,
        sample_annotations=sample_annotations,
        sample_data_list=sample_data_list,
        scenes=scenes,
        sensors=[ARTERY_CONSTANTS.sensor_lidar_top],
        visibility=ARTERY_CONSTANTS.visibility,
    )
    return nuscenes_reference


def get_ego_poses(artery_sim_log: ArterySimLog) -> list[EgoPose]:
    ego_poses: list[EgoPose] = []

    for ego_frame in artery_sim_log.ego_vehicle:
        ego_pose = EgoPose(
            token=Guid(),
            timestamp=ego_frame["origin"]["timestamp"],
            rotation=Quaternion(heading=ego_frame["heading"]["value"]),
            translation=_get_translation(artery_object=ego_frame),
        )
        ego_poses.append(ego_pose)

    return ego_poses


def get_log(logfile_name: str) -> Log:
    return Log(
        token=Guid(),
        logfile=logfile_name,
        vehicle=ARTERY_CONSTANTS.log_vehicle,
        date_captured=ARTERY_CONSTANTS.log_date_captured,
        location=ARTERY_CONSTANTS.log_location,
    )


def get_map(nuscenes_version_dirname: str, log_tokens: list[Guid], png_bytes: bytes) -> Map:
    return Map(
        token=Guid(),
        category=ARTERY_CONSTANTS.map_category,
        png_bytes=png_bytes,
        filename=os.path.join(nuscenes_version_dirname, ARTERY_CONSTANTS.map_filename),
        log_tokens=log_tokens,
    )


def _get_translation(artery_object: ArteryObject) -> Vector3:
    return Vector3(
        value=[artery_object["loc"][0]["value"], artery_object["loc"][1]["value"], artery_object["loc"][2]["value"]]
    )


def _get_size(artery_object: ArteryObject) -> Vector3:
    # Order: [width, length, height] both in artery and nuscenes
    return Vector3(
        value=[artery_object["dim"][0]["value"], artery_object["dim"][1]["value"], artery_object["dim"][2]["value"]]
    )


def _get_velocity(artery_object: ArteryObject) -> Vector2:
    return Vector2(
        value=[
            cos(artery_object["heading"]["value"]) * artery_object["speed"]["value"],
            sin(artery_object["heading"]["value"]) * artery_object["speed"]["value"],
        ]
    )


def _get_attribute(artery_object: ArteryObject) -> Guid:
    MOVING_THRESHOLD = 0.01  # m/s

    if fabs(artery_object["speed"]["value"]) < MOVING_THRESHOLD:
        return ARTERY_CONSTANTS.attribute_vehicle_stopped.token
    else:
        return ARTERY_CONSTANTS.attribute_vehicle_moving.token


def _get_sample_token(samples: list[Sample], timestamp: int) -> Guid:
    for sample in samples:
        if sample.timestamp == timestamp:
            return sample.token
    raise ValueError(f"Timestamp {timestamp} not found in samples")


def _get_ego_pose_token(ego_poses: list[EgoPose], timestamp: int) -> Guid:
    for ego_pose in ego_poses:
        if ego_pose.timestamp == timestamp:
            return ego_pose.token
    raise ValueError(f"Timestamp {timestamp} not found in ego poses")


def dump_white_map_mask_png(file_path: str):
    """Nuscenes uses a map file that is color-coded to represent the area relevant for traffic.
    White is foreground (roads and sidewalks) and black is background (the rest).

    It looks like the nuscenes map has a default resolution of 0.1m per pixel.
    Its coordinate origin is in the top left corner of the image.

    :param file_path: Path to the map file relative to nuscenes dataroot."""

    resolution = 0.1  # meters per pixel
    width_meters = 1000  # meters
    height_meters = 1000  # meters
    width_pixels = int(width_meters / resolution)
    heigh_pixels = int(height_meters / resolution)

    white_image = Image.new("RGB", (width_pixels, heigh_pixels), "white")
    white_image.save(file_path)


def get_objects_and_frames(
    artery_sim_log: ArterySimLog, samples: list[Sample], ego_poses: list[EgoPose]
) -> tuple[list[SampleAnnotation], list[SampleData], list[Instance]]:
    """Get data of dynamic reference objects and frames all in one function because they
    are interdependent"""

    sample_data_list: list[SampleData] = []
    sample_annotations: list[SampleAnnotation] = []
    instances: list[Instance] = []

    for artery_trajectory in artery_sim_log.objects_res.values():
        if len(artery_trajectory) == 0:
            continue

        instance_token: Guid = Guid()

        frames_of_instance_counter: int = 0
        for artery_object in artery_trajectory:
            first_frame = frames_of_instance_counter == 0
            last_frame = frames_of_instance_counter == len(artery_trajectory) - 1

            sample_token = _get_sample_token(samples=samples, timestamp=artery_object["origin"]["timestamp"])

            sample_annotation = SampleAnnotation(
                token=Guid() if first_frame else sample_annotations[-1].next,
                sample_token=sample_token,
                instance_token=instance_token,
                visibility_token=ARTERY_CONSTANTS.visibility_full.token,
                prev=Guid("") if first_frame else sample_annotations[-1].token,
                next=Guid() if not last_frame else Guid(""),  # set guid of next frame already here
                num_lidar_pts=ARTERY_CONSTANTS.default_num_points_annotation,
                num_radar_pts=ARTERY_CONSTANTS.default_num_points_annotation,
                translation=_get_translation(artery_object=artery_object),
                size=_get_size(artery_object=artery_object),
                rotation=Quaternion(heading=artery_object["heading"]["value"]),
                attribute_tokens=[_get_attribute(artery_object=artery_object)],
            )
            sample_annotations.append(sample_annotation)

            sample_data = SampleData(
                token=Guid() if first_frame else sample_data_list[-1].next,
                sample_token=sample_token,
                ego_pose_token=_get_ego_pose_token(ego_poses=ego_poses, timestamp=artery_object["origin"]["timestamp"]),
                calibrated_sensor_token=ARTERY_CONSTANTS.calibrated_sensor_lidar_top.token,
                timestamp=artery_object["origin"]["timestamp"],
                fileformat="artery",
                is_key_frame=True,  #  all frames are key frames -> all frames will be evaluated
                height=0,
                width=0,
                filename="no_raw_data_available",
                prev=Guid("") if first_frame else sample_data_list[-1].token,
                next=Guid() if not last_frame else Guid(""),  # set guid of next frame already here
            )
            sample_data_list.append(sample_data)

            frames_of_instance_counter += 1

        instance = Instance(
            token=instance_token,
            category_token=ARTERY_CONSTANTS.category_car.token,
            nbr_annotations=len(artery_trajectory),
            first_annotation_token=sample_annotations[-len(artery_trajectory)].token,
            last_annotation_token=sample_annotations[-1].token,
        )
        instances.append(instance)

    return sample_annotations, sample_data_list, instances


def get_samples_and_scenes(artery_sim_log: ArterySimLog, log_token: Guid) -> tuple[list[Sample], list[Scene]]:
    scene_token = Guid()  # same scene for all samples

    samples: list[Sample] = []

    timestamp_counter: int = 0
    for timestamp in artery_sim_log.timestamps:
        first_stamp = timestamp_counter == 0
        last_stamp = timestamp_counter == (len(artery_sim_log.timestamps) - 1)

        sample = Sample(
            token=Guid() if first_stamp else samples[-1].next,
            timestamp=timestamp,
            prev=Guid("") if first_stamp else samples[-1].token,
            next=Guid() if not last_stamp else Guid(""),  # set guid of next sample already here
            scene_token=scene_token,
        )
        samples.append(sample)

        timestamp_counter += 1

    scenes = [
        Scene(
            token=scene_token,
            log_token=log_token,
            nbr_samples=len(artery_sim_log.timestamps),
            first_sample_token=samples[0].token,
            last_sample_token=samples[-1].token,
            name=artery_sim_log.name,
            description="Converted scene from an artery simulation log",
        )
    ]
    return samples, scenes


def get_nuscenes_submission(artery_sim_log: ArterySimLog, samples: list[Sample]) -> TrackingSubmission:
    sample_results: TrackingResults = get_sample_results_over_frames(artery_sim_log=artery_sim_log, samples=samples)

    tracking_submission = TrackingSubmission(
        token=Guid(), meta=ARTERY_CONSTANTS.tracking_submission_meta, results=sample_results
    )
    return tracking_submission


def get_sample_results_over_frames(artery_sim_log: ArterySimLog, samples: list[Sample]) -> TrackingResults:
    """TrackingResults maps each sample_token (frame) to a list of sample_results (perceived objects)."""
    sample_results: TrackingResults = {}

    for artery_object_id, artery_trajectory in artery_sim_log.objects_out.items():
        if len(artery_trajectory) == 0:
            continue

        tracking_id: str = str(artery_object_id)

        for artery_object in artery_trajectory:
            sample_token = _get_sample_token(samples=samples, timestamp=artery_object["origin"]["timestamp"])

            if sample_token not in sample_results:
                sample_results[sample_token] = []

            sample_result = SampleResult(
                tracking_id=tracking_id,
                sample_token=sample_token,
                tracking_name=ARTERY_CONSTANTS.default_trackig_name,
                tracking_score=ARTERY_CONSTANTS.default_tracking_score,
                translation=_get_translation(artery_object=artery_object),
                size=_get_size(artery_object=artery_object),
                rotation=Quaternion(heading=artery_object["heading"]["value"]),
                velocity=_get_velocity(artery_object=artery_object),
            )
            sample_results[sample_token].append(sample_result)

    return sample_results


def dump_to_nuscenes_dir(nuscenes_all: NuScenesAll, nuscenes_version_dir: str, force_overwrite: bool = False) -> None:
    """Dump all data to json files in the nuscenes version directory."""
    common_indent: int = 2

    # Prepare empty output directory
    if os.path.isdir(nuscenes_version_dir):
        if os.listdir(nuscenes_version_dir) != []:  # directory is not empty
            if force_overwrite:
                shutil.rmtree(nuscenes_version_dir)  # also deletes nuscenes_dir itself
            else:
                raise ValueError(
                    f"Directory {nuscenes_version_dir} already exists. Set force_overwrite=True to clear it."
                )
    os.makedirs(nuscenes_version_dir, exist_ok=False)

    # Dump reference data
    def _dump_to_json_file(dataclass_objects: Sequence[NuScenesWritable], custom_filename: Optional[str] = None):
        list_of_dicts = [dataclass_object.to_dict() for dataclass_object in dataclass_objects]

        filename = custom_filename or dataclass_objects[0].json_filename
        json_path = os.path.join(nuscenes_version_dir, filename)
        with open(json_path, "w") as json_file:
            json.dump(list_of_dicts, json_file, indent=common_indent)

    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.attributes)
    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.calibrated_sensors)
    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.categories)
    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.ego_poses)
    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.instances)
    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.logs)
    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.maps)
    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.samples)
    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.sample_annotations)
    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.sample_data_list)
    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.scenes)
    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.sensors)
    _dump_to_json_file(dataclass_objects=nuscenes_all.reference.visibility)

    # Dump splits
    splits_json_path = os.path.join(nuscenes_version_dir, Split.json_filename)
    with open(splits_json_path, "w") as json_file:
        json.dump(get_splits_dict(nuscenes_all.splits), json_file, indent=common_indent)

    # Dump submission data
    submission_json_path = os.path.join(nuscenes_version_dir, nuscenes_all.submission.json_filename)
    with open(submission_json_path, "w") as json_file:
        json.dump(nuscenes_all.submission.to_dict(), json_file, indent=common_indent)

    # Dump map file
    # map_path = os.path.join(nuscenes_version_dir, ARTERY_CONSTANTS.map_filename)
    for map in nuscenes_all.reference.maps:
        # avoid ns  version dir twice in the path
        png_path = os.path.normpath(os.path.join(nuscenes_version_dir, "..", map.filename))
        with open(png_path, "wb") as f:
            f.write(map.png_bytes)
