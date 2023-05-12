from inputs.nuscenes.nuscenes_format import NuScenesAll


def get_submitted_track_lenghts(nuscenes_all: NuScenesAll) -> dict[str, int]:
    """returns a dict from track id to track length (measured in total available frames of that id)"""
    tracks = {}

    for frame in nuscenes_all.submission.results.values():
        for object_out in frame:
            if object_out.tracking_id not in tracks:
                tracks[object_out.tracking_id] = 1
            else:
                tracks[object_out.tracking_id] = tracks[object_out.tracking_id] + 1
    return tracks


def get_reference_track_lenghts(nuscenes_all: NuScenesAll) -> dict[str, int]:
    """returns a dict from track id to track length (measured in total available frames of that id)"""
    tracks = {str(instance.token): instance.nbr_annotations for instance in nuscenes_all.reference.instances}
    return tracks
