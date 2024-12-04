from commonroad.common.file_reader import CommonRoadFileReader  # type: ignore
from commonroad.visualization.mp_renderer import MPRenderer  # type: ignore

from research.delta_crit.crime_utils.crime_utils import get_scenario_xml

scenario_id = "DEU_Gar-1_1_T-1"
scenario_file_path = get_scenario_xml(scenario_id=scenario_id)

scenario, planning_problem_set = CommonRoadFileReader(scenario_file_path).open()

# plot the scenario
rnd = MPRenderer(figsize=(25, 10))
scenario.draw(rnd)
rnd.render(show=True)
pass
