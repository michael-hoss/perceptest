import sys
from typing import Optional

import pytest

from inputs.artery.artery_format import ArteryObject, ArterySimLog
from inputs.artery.from_logs.timestamps import (
    _find_index_of_fuzzy_value,
    _get_timestamps,
    _trim_to_time_range,
    tidy_up_timestamps,
)


@pytest.fixture
def example_trajectory() -> list:
    # Leave out the other fields of ArteryObject for simplicity
    return [
        {"origin": {"timestamp": 1}},
        {"origin": {"timestamp": 3}},
        {"origin": {"timestamp": 5}},
    ]


def _get_dummy_object(timestamp: Optional[int]) -> ArteryObject:
    timestamp = timestamp or 0
    artery_object: ArteryObject = {
        "origin": {"id": 0, "idlocal": 0, "timestamp": timestamp},
        "unit": "Digital,MV_Global",
        "loc": [{"value": 0, "uncertainty": 0}, {"value": 0, "uncertainty": 0}, {"value": 0, "uncertainty": 0}],
        "speed": {"value": 0, "uncertainty": 0},
        "heading": {"value": 0, "uncertainty": 0},
        "yaw_rate": {"value": 0, "uncertainty": 0},
        "acceleration": {"value": 0, "uncertainty": 0},
        "dim": [{"value": 0, "uncertainty": 0}, {"value": 0, "uncertainty": 0}, {"value": 0, "uncertainty": 0}],
        "orientation": {"value": 0, "uncertainty": 0},
        "steering": {"value": 0, "uncertainty": 0},
        "parking": False,
    }
    return artery_object


def _get_dummy_trajectory(timestamps: list[int]) -> list[ArteryObject]:
    return [_get_dummy_object(timestamp=timestamp) for timestamp in timestamps]


def test__find_index_of_fuzzy_value() -> None:
    assert _find_index_of_fuzzy_value([1, 3, 5], 0, use_smaller=True) == 0
    assert _find_index_of_fuzzy_value([1, 3, 5], 1, use_smaller=True) == 0
    assert _find_index_of_fuzzy_value([1, 3, 5], 2, use_smaller=True) == 0
    assert _find_index_of_fuzzy_value([1, 3, 5], 3, use_smaller=True) == 1
    assert _find_index_of_fuzzy_value([1, 3, 5], 4, use_smaller=True) == 1
    assert _find_index_of_fuzzy_value([1, 3, 5], 5, use_smaller=True) == 2
    assert _find_index_of_fuzzy_value([1, 3, 5], 6, use_smaller=True) == 2

    assert _find_index_of_fuzzy_value([1, 3, 5], 0, use_smaller=False) == 0
    assert _find_index_of_fuzzy_value([1, 3, 5], 1, use_smaller=False) == 0
    assert _find_index_of_fuzzy_value([1, 3, 5], 2, use_smaller=False) == 1
    assert _find_index_of_fuzzy_value([1, 3, 5], 3, use_smaller=False) == 1
    assert _find_index_of_fuzzy_value([1, 3, 5], 4, use_smaller=False) == 2
    assert _find_index_of_fuzzy_value([1, 3, 5], 5, use_smaller=False) == 2
    assert _find_index_of_fuzzy_value([1, 3, 5], 6, use_smaller=False) == 2


def test__trim_to_time_range_full(example_trajectory: list[ArteryObject]) -> None:
    assert _trim_to_time_range(trajectory=example_trajectory, begin=0, end=6) == [
        {"origin": {"timestamp": 1}},
        {"origin": {"timestamp": 3}},
        {"origin": {"timestamp": 5}},
    ]


def test__trim_to_time_range_before(example_trajectory: list[ArteryObject]) -> None:
    assert _trim_to_time_range(trajectory=example_trajectory, begin=-5, end=0) == []


def test__trim_to_time_range_after(example_trajectory: list[ArteryObject]) -> None:
    assert _trim_to_time_range(trajectory=example_trajectory, begin=6, end=10) == []


def test__trim_to_time_range_edge_before(example_trajectory: list[ArteryObject]) -> None:
    assert _trim_to_time_range(trajectory=example_trajectory, begin=-5, end=1) == [
        {"origin": {"timestamp": 1}},
    ]


def test__trim_to_time_range_edge_after(example_trajectory: list[ArteryObject]) -> None:
    assert _trim_to_time_range(trajectory=example_trajectory, begin=5, end=10) == [
        {"origin": {"timestamp": 5}},
    ]


def test__trim_to_time_range_fuzzy_before(example_trajectory: list[ArteryObject]) -> None:
    assert _trim_to_time_range(trajectory=example_trajectory, begin=0, end=2) == [
        {"origin": {"timestamp": 1}},
    ]


def test__trim_to_time_range_fuzzy_after(example_trajectory: list[ArteryObject]) -> None:
    assert _trim_to_time_range(trajectory=example_trajectory, begin=4, end=6) == [
        {"origin": {"timestamp": 5}},
    ]


def test__trim_to_time_range_fuzzy_middle(example_trajectory: list[ArteryObject]) -> None:
    assert _trim_to_time_range(trajectory=example_trajectory, begin=2, end=4) == [
        {"origin": {"timestamp": 3}},
    ]


def test_map_to_common_timestamps_ego_in_middle() -> None:
    # Prepare input data
    objects_out = {
        1: _get_dummy_trajectory([1, 3, 5]),
    }
    objects_res = {
        2: _get_dummy_trajectory([1, 3]),
    }
    ego_vehicle = _get_dummy_trajectory([3])
    artery_sim_log = ArterySimLog(
        objects_out=objects_out, objects_res=objects_res, ego_vehicle=ego_vehicle, timestamps=[]
    )

    # Function under test
    tidy_up_timestamps(artery_sim_log=artery_sim_log)

    # Assertions
    assert artery_sim_log.timestamps == [3]
    assert _get_timestamps(artery_sim_log.objects_out[1]) == [3]
    assert _get_timestamps(artery_sim_log.objects_res[2]) == [3]


def test_map_to_common_timestamps_no_overlap() -> None:
    # Prepare input data
    objects_out = {
        1: _get_dummy_trajectory([1, 3, 5]),
    }
    objects_res = {
        2: _get_dummy_trajectory([1, 3]),
    }
    ego_vehicle = _get_dummy_trajectory([7, 9])
    artery_sim_log = ArterySimLog(
        objects_out=objects_out, objects_res=objects_res, ego_vehicle=ego_vehicle, timestamps=[]
    )

    # Function under test
    with pytest.raises(ValueError, match="No common time range found."):
        tidy_up_timestamps(artery_sim_log=artery_sim_log)


def test_map_to_common_timestamps_fuzzy() -> None:
    # Prepare input data
    objects_out = {
        1: _get_dummy_trajectory([2, 4, 6]),
    }
    objects_res = {
        2: _get_dummy_trajectory([2, 4, 6, 8]),
    }
    ego_vehicle = _get_dummy_trajectory([1, 3, 5])
    artery_sim_log = ArterySimLog(
        objects_out=objects_out, objects_res=objects_res, ego_vehicle=ego_vehicle, timestamps=[]
    )

    # Function under test
    tidy_up_timestamps(artery_sim_log=artery_sim_log, expect_no_shift=False)

    # Assertions
    # Expect cutoff of OuT and ReS data at beginning and end, and shift onto subsequent ego stamps.
    assert artery_sim_log.timestamps == [3, 5]
    assert _get_timestamps(artery_sim_log.objects_out[1]) == [3, 5]
    assert _get_timestamps(artery_sim_log.objects_res[2]) == [3, 5]
    assert _get_timestamps(artery_sim_log.ego_vehicle) == [3, 5]


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
