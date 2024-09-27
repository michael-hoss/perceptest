import itertools
import json
import os
import shutil
from typing import Optional, Sequence

from inputs.nuscenes.nuscenes_format import (
    Guid,
    Map,
    NuScenesAll,
    NuScenesReference,
    NuScenesWritable,
    Split,
    TrackingResults,
    TrackingSubmission,
    get_splits_dict,
)


def merge_nuscenes_submissions(tracking_submissions_list: list[TrackingSubmission]) -> TrackingSubmission:
    assert_all_elements_equal([tracking_submission.meta for tracking_submission in tracking_submissions_list])

    all_results: list[TrackingResults] = [
        tracking_submission.results for tracking_submission in tracking_submissions_list
    ]

    merged_results: TrackingResults = merge_dicts(all_results)

    return TrackingSubmission(token=Guid(), meta=tracking_submissions_list[0].meta, results=merged_results)


def merge_nuscenes_references(nuscenes_references_list: list[NuScenesReference]) -> NuScenesReference:
    # For simplicity, these fields are assumed to be equal anyway.
    assert_all_elements_equal([ns_ref.attributes for ns_ref in nuscenes_references_list])
    assert_all_elements_equal([ns_ref.calibrated_sensors for ns_ref in nuscenes_references_list])
    assert_all_elements_equal([ns_ref.categories for ns_ref in nuscenes_references_list])
    assert_all_elements_equal([ns_ref.sensors for ns_ref in nuscenes_references_list])
    assert_all_elements_equal([ns_ref.visibility for ns_ref in nuscenes_references_list])

    return NuScenesReference(
        attributes=nuscenes_references_list[0].attributes,
        calibrated_sensors=nuscenes_references_list[0].calibrated_sensors,
        categories=nuscenes_references_list[0].categories,
        ego_poses=flatten_list([ns_ref.ego_poses for ns_ref in nuscenes_references_list]),  # type: ignore
        instances=flatten_list([ns_ref.instances for ns_ref in nuscenes_references_list]),  # type: ignore
        logs=flatten_list([ns_ref.logs for ns_ref in nuscenes_references_list]),  # type: ignore
        maps=merge_nuscenes_maps([ns_ref.maps for ns_ref in nuscenes_references_list]),
        samples=flatten_list([ns_ref.samples for ns_ref in nuscenes_references_list]),  # type: ignore
        sample_annotations=flatten_list([ns_ref.sample_annotations for ns_ref in nuscenes_references_list]),  # type: ignore
        sample_data_list=flatten_list([ns_ref.sample_data_list for ns_ref in nuscenes_references_list]),  # type: ignore
        scenes=flatten_list([ns_ref.scenes for ns_ref in nuscenes_references_list]),  # type: ignore
        sensors=nuscenes_references_list[0].sensors,
        visibility=nuscenes_references_list[0].visibility,
    )


def merge_nuscenes_maps(list_of_lists: list[list[Map]]) -> list[Map]:
    """Merges equal maps with incomplete log tokens into a single map containing all log tokens.
    Operates on lists of all of this because nuScenes expects this."""

    flattened_maps: list[Map] = flatten_list(list_of_lists)  # type: ignore

    if len(flattened_maps) == 0:
        return []

    # Expect each incoming NuScenesReference to have exactly one map
    assert len(flattened_maps) == len(list_of_lists)

    assert_all_elements_equal([map.category for map in flattened_maps])
    assert_all_elements_equal([map.filename for map in flattened_maps])
    assert_all_elements_equal([map.png_bytes for map in flattened_maps])

    all_log_tokens = []
    for map in flattened_maps:
        all_log_tokens.extend(map.log_tokens)

    merged_map: Map = Map(
        token=Guid(),
        category=flattened_maps[0].category,
        filename=flattened_maps[0].filename,
        png_bytes=flattened_maps[0].png_bytes,
        log_tokens=all_log_tokens,
    )
    return [merged_map]


def merge_nuscenes_splits(splits_list: list[list[Split]]) -> list[Split]:
    flattened_splits = list(itertools.chain.from_iterable(splits_list))

    # Merge the "all" splits
    tidied_splits = [split for split in flattened_splits if split.name != "all"]
    merged_scene_names = list(itertools.chain.from_iterable([split.scene_names for split in tidied_splits]))
    merged_all_split = Split(name="all", scene_names=merged_scene_names)
    tidied_splits.append(merged_all_split)

    # Assert no duplicate splits and split names
    all_split_names: list[str] = [split.name for split in tidied_splits]
    assert len(tidied_splits) == len(set(tidied_splits))
    assert len(all_split_names) == len(set(all_split_names))

    return tidied_splits


def merge_nuscenes_all(nuscenes_all_list: list[NuScenesAll]) -> NuScenesAll:
    nuscenes_all_combined = NuScenesAll(
        reference=merge_nuscenes_references([nuscenes_all.reference for nuscenes_all in nuscenes_all_list]),
        submission=merge_nuscenes_submissions([nuscenes_all.submission for nuscenes_all in nuscenes_all_list]),
        splits=merge_nuscenes_splits([nuscenes_all.splits for nuscenes_all in nuscenes_all_list]),
    )
    return nuscenes_all_combined


def assert_all_elements_equal(iterable: list) -> None:
    assert all(element == iterable[0] for element in iterable)


def merge_dicts(list_of_dicts: list[dict]) -> dict:
    """Asserts that the keys of all input dicts are unique and merges them into one dict."""
    num_dict_keys_before_merge = sum(len(my_dict) for my_dict in list_of_dicts)

    merged_dict = {}
    for d in list_of_dicts:
        merged_dict.update(d)

    assert num_dict_keys_before_merge == len(merged_dict)
    return merged_dict


def flatten_list(list_of_lists: list[list[NuScenesWritable]]) -> list:
    if len(list_of_lists) == 0:
        return []

    flattened_list = list(itertools.chain.from_iterable(list_of_lists))
    assert_unique_tokens(flattened_list)
    return flattened_list


def assert_unique_tokens(my_list: list[NuScenesWritable]) -> None:
    tokens = [item.token for item in my_list]
    assert len(tokens) == len(set(tokens)), f"Tokens are not unique: {tokens}"


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
