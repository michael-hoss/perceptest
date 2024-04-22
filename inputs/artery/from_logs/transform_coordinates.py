from math import pi
from typing import Optional, Sequence

from base.geo_coordinates.geo_coordinates import WGS84Transformer
from inputs.artery.artery_format import ArteryObject, ArterySimLog


def transform_to_local_metric_coords(
    artery_sim_log: ArterySimLog, origin_lat: Optional[float] = None, origin_lon: Optional[float] = None
) -> ArterySimLog:
    # Use one transformer so the same UTM zone is used for all transformations
    transformer = WGS84Transformer(origin_lat=origin_lat, origin_lon=origin_lon)

    # Transform locations from WGS84 to local metric coordinates (using UTM)
    for out_object_traj in artery_sim_log.objects_out.values():
        transform_object_traj_to_local_metric_coords(object_traj=out_object_traj, transformer=transformer)
    for res_object_traj in artery_sim_log.objects_res.values():
        transform_object_traj_to_local_metric_coords(object_traj=res_object_traj, transformer=transformer)
    artery_sim_log.ego_vehicle = transform_object_traj_to_local_metric_coords(  # type: ignore
        object_traj=artery_sim_log.ego_vehicle, transformer=transformer
    )
    return artery_sim_log


def transform_object_traj_to_local_metric_coords(
    object_traj: Sequence[ArteryObject], transformer: WGS84Transformer
) -> Sequence[ArteryObject]:
    microradiants_to_degrees = 1e-7 * 180 / pi  # HACK: should be 1e-6, we will figure out conversion error.
    for object_frame in object_traj:
        longitude_deg = object_frame["loc"][0]["value"] * microradiants_to_degrees
        latitude_deg = object_frame["loc"][1]["value"] * microradiants_to_degrees
        easting, northing = transformer.transform_wgs84_to_local_metric(longitude=longitude_deg, latitude=latitude_deg)
        object_frame["loc"][0]["value"] = easting
        object_frame["loc"][1]["value"] = northing

        # HACK until @MatLucena fixes it in the artery export
        # Make heading aligned to zero-east, counter-clockwise positive
        # insteadd of zero-north, clockwise positive
        object_frame["heading"]["value"] = -object_frame["heading"]["value"] + 0.5 * pi
        while object_frame["heading"]["value"] < 0:
            object_frame["heading"]["value"] += 2 * pi
    return object_traj
