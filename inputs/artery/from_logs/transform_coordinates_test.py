import sys
from typing import Sequence

import pytest

from base.geometry.aa_bounding_box import AABoundingBox
from inputs.artery.artery_format import ArteryData, ArteryObject
from inputs.artery.from_logs.transform_coordinates import transform_to_local_metric_coords


def get_outer_hull_of_all_locations(
    artery_object_traj: Sequence[ArteryObject],
) -> AABoundingBox:
    # X=easting, Y=northing
    actual_bounds = AABoundingBox()

    for object_frame in artery_object_traj:
        assert len(object_frame["loc"]) == 3
        actual_bounds.include_point(x=object_frame["loc"][0]["value"], y=object_frame["loc"][1]["value"])

    return actual_bounds


def test_transform_to_meters_pass(artery_data: ArteryData) -> None:
    """This test rather tests the data than the code."""

    # Function under test
    artery_data = transform_to_local_metric_coords(artery_data=artery_data)

    # Assertions
    assert isinstance(artery_data, ArteryData)

    # Get the bounds of the ReS coordinates
    actual_bounds_res_objects = AABoundingBox()
    for res_object_traj in artery_data.objects_res.values():
        current_bounds: AABoundingBox = get_outer_hull_of_all_locations(artery_object_traj=res_object_traj)
        actual_bounds_res_objects.include_aa_bounding_box(other=current_bounds)

    # Get the bounds of the OuT coordinates
    actual_bounds_out_objects = AABoundingBox()
    for out_object_traj in artery_data.objects_out.values():
        current_bounds = get_outer_hull_of_all_locations(artery_object_traj=out_object_traj)
        actual_bounds_out_objects.include_aa_bounding_box(other=current_bounds)

    # Get the bounds of the ego vehicle coordinates
    actual_bounds_ego_vehicle: AABoundingBox = get_outer_hull_of_all_locations(
        artery_object_traj=artery_data.ego_vehicle
    )

    # Lenghts in meters. The numbers are from the sumo description of the coordinates.
    # Boundaries from v5 onwards:
    """
    <location netOffset="0.00,0.00"
    convBoundary="0.00,0.00,375.00,375.00"
    origBoundary="0.00,0.00,375.00,375.00"
    projParameter="+proj=tmerc +ellps=WGS84 +datum=WGS84 +units=m +no_defs"/>
    """
    tolerance: float = 20
    expected_outer_bounds = AABoundingBox(
        x_min=0 - tolerance,
        x_max=375 + tolerance,
        y_min=0 - tolerance,
        y_max=375 + tolerance,
    )

    assert actual_bounds_res_objects.is_contained_in(outer=expected_outer_bounds)
    assert actual_bounds_out_objects.is_contained_in(outer=expected_outer_bounds)
    assert actual_bounds_ego_vehicle.is_contained_in(outer=expected_outer_bounds)

    expected_min_span: float = 100
    assert actual_bounds_res_objects.is_larger_than_min_span(x=expected_min_span, y=expected_min_span)
    assert actual_bounds_out_objects.is_larger_than_min_span(x=expected_min_span, y=expected_min_span)

    # No min span requirement for the ego vehicle in x or y
    # because it might just move completely parallel to one coordinate axis.


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(pytest.main([__file__, "-vv"] + args))
