from commonroad_crime.data_structure.configuration import CriMeConfiguration
from commonroad_crime.data_structure.crime_interface import CriMeInterface
from commonroad_crime.measure import (
    BTN,
    HW,
    P_MC,
    PF,
    STN,
    THW,
    TTB,
    TTC,
    TTK,
    TTR,
    TTS,
    WTTC,
    ALatReq,
    ALongReq,
    DeltaV,
    LatJ,
    LongJ,
    TTCStar,
)

# ==== specify scenario ID
scenario_id = "DEU_Gar-1_1_T-1"

# ==== build configuration
# TODO: INCLUDE commonroad-crime as submodule, build it from source, and then also take the config file
# from there!
config = CriMeConfiguration.load(f"../config_files/{scenario_id}.yaml", scenario_id)
# or use the default one with: config = CriMeConfiguration()
config.update()
config.print_configuration_summary()

# ==== compute the criticality using CriMe interface
crime_interface = CriMeInterface(config)
crime_interface.evaluate_scenario(
    [HW, THW, TTC, WTTC, TTCStar, TTS, TTK, TTB, TTR, ALongReq, ALatReq, LongJ, LatJ, DeltaV, BTN, STN, P_MC, PF],
)  # and more ...

# ==== visualize the results for debugging and showcasing
crime_interface.visualize()
