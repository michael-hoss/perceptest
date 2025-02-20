from commonroad_crime.data_structure.crime_interface import CriMeInterface  # type: ignore


def compute_delta(sut: CriMeInterface, res: CriMeInterface) -> dict:
    """Compute the differences C_sut - C_res for all criticality measures C in all time steps."""

    delta_dict: dict = {}

    for time_step in range(res.time_start, res.time_end + 1):
        delta_dict[time_step] = {}

        for measure in res.measures:
            measure_name: str = measure.measure_name.value

            delta_dict[time_step][measure_name] = (
                sut.criticality_dict[time_step][measure_name] - res.criticality_dict[time_step][measure_name]
            )

    return delta_dict
