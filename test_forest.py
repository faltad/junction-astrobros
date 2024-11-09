from packages.models import Coords, Seasons
from packages.sentinel import (
    get_forestation_analysis,
    process_forest_data_generate_deforestation_rate_graph,
    process_forest_data_generate_visualisation,
)
import config


def run():
    settings = config.Settings()
    get_forestation_analysis(
        settings.prepare_sh_config(),
        season=Seasons.SUMMER,
        coords=Coords(latitude=1, longitude=1),
    )
    process_forest_data_generate_deforestation_rate_graph()
    process_forest_data_generate_visualisation()


if __name__ == "__main__":
    run()
