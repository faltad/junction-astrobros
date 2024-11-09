from packages.sentinel import (
    process_forest_data_generate_visualisation,
)
import config


def run():
    settings = config.Settings()
    # get_forestation_analysis(
    #     settings.prepare_sh_config(),
    #     season=Seasons.SUMMER,
    #     coords=Coords(
    #         south_east_latitude=1,
    #         south_east_longitude=1,
    #         north_west_latitude=1,
    #         north_west_longitude=1,
    #     ),
    # )
    # process_forest_data_generate_deforestation_rate_graph()
    out = process_forest_data_generate_visualisation()
    print(str(out))


if __name__ == "__main__":
    run()
