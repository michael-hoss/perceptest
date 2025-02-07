from commonroad.scenario.scenario import Scenario  # type: ignore

from research.delta_crit.crime_utils.create_dynamic_obstacle import create_steady_dynamic_obstacle
from research.delta_crit.crime_utils.refresh_dynamic_obstacles import refresh_dynamic_obstacles


def strip_down_to_test_scenario(
    scenario: Scenario, ego_id: int, targets_east: float = 10, targets_north: float = 0
) -> Scenario:
    """Create a minimal scenario with ego vehicle at 0,0 and all other dynamic obstacles at targets_east, targets_north. Otherwise, default values."""

    target_ids: list[int] = [obs.obstacle_id for obs in scenario.dynamic_obstacles if obs.obstacle_id != ego_id]

    scenario.remove_obstacle(scenario.dynamic_obstacles)

    ego_vehicle = create_steady_dynamic_obstacle(obstacle_id=ego_id)
    scenario.add_objects(ego_vehicle)

    for target_id in target_ids:
        target_vehicle = create_steady_dynamic_obstacle(
            obstacle_id=target_id, position_x=targets_east, position_y=targets_north
        )
        scenario.add_objects(target_vehicle)

    refresh_dynamic_obstacles(scenario=scenario)
    return scenario
