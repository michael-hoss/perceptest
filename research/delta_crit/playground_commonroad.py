from research.delta_crit.crime_utils.crime_utils import (
    visualize_time_steps,
)


def main():
    # visualize_statically("DEU_Gar-1_1_T-1")
    visualize_time_steps("DEU_Gar-1_1_T-1", [0, 20])
    # visualize_time_steps("OSC_CutIn-1_2_T-1", [20, 34, 99])

    # visualize_statically("OSC_Overtake-1_1_T-1")
    visualize_time_steps("OSC_Overtake-1_1_T-1", [0, 10, 20])
    visualize_time_steps("OSC_Overtake-1_1_T-1", [69, 121, 129])  # needs larger plot limits!

    pass


if __name__ == "__main__":
    main()
