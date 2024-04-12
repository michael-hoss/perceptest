import itertools

from inputs.nuscenes.nuscenes_format import (
    Guid,
    NuScenesAll,
    NuScenesReference,
    NuScenesWritable,
    Split,
    TrackingResults,
    TrackingSubmission,
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
    assert_all_elements_equal([ns_ref.maps for ns_ref in nuscenes_references_list])
    assert_all_elements_equal([ns_ref.sensors for ns_ref in nuscenes_references_list])
    assert_all_elements_equal([ns_ref.visibility for ns_ref in nuscenes_references_list])

    return NuScenesReference(
        attributes=nuscenes_references_list[0].attributes,
        calibrated_sensors=nuscenes_references_list[0].calibrated_sensors,
        categories=nuscenes_references_list[0].categories,
        ego_poses=flatten_list([ns_ref.ego_poses for ns_ref in nuscenes_references_list]),  # type: ignore
        instances=flatten_list([ns_ref.instances for ns_ref in nuscenes_references_list]),  # type: ignore
        logs=flatten_list([ns_ref.logs for ns_ref in nuscenes_references_list]),  # type: ignore
        maps=nuscenes_references_list[0].maps,
        samples=flatten_list([ns_ref.samples for ns_ref in nuscenes_references_list]),  # type: ignore
        sample_annotations=flatten_list([ns_ref.sample_annotations for ns_ref in nuscenes_references_list]),  # type: ignore
        sample_data_list=flatten_list([ns_ref.sample_data_list for ns_ref in nuscenes_references_list]),  # type: ignore
        scenes=flatten_list([ns_ref.scenes for ns_ref in nuscenes_references_list]),  # type: ignore
        sensors=nuscenes_references_list[0].sensors,
        visibility=nuscenes_references_list[0].visibility,
    )


def merge_nuscenes_splits(splits_list: list[list[Split]]) -> list[Split]:
    flattened_splits = list(itertools.chain.from_iterable(splits_list))
    assert len(flattened_splits) == len(set(flattened_splits))  # Assert no duplicate split names
    return flattened_splits


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
