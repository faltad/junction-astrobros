import base64
import config
from packages.models import Coords, Seasons
from packages.sentinel import (
    get_forestation_analysis,
    process_forest_data_generate_deforestation_rate_graph,
)


def run():
    settings = config.Settings()
    get_forestation_analysis(
        settings.prepare_sh_config(),
        season=Seasons.SUMMER,
        coords=Coords(
            south_west_latitude=24.3917701,
            south_west_longitude=60.246912,
            north_east_latitude=24.729401,
            north_east_longitude=60.364885,
        ),
    )
    # process_forest_data_generate_visualisation()
    out = process_forest_data_generate_deforestation_rate_graph()
    print(base64.b64encode(out.read()).decode("utf-8"))
    print(str(out))


if __name__ == "__main__":
    run()


"""
curl 'http://localhost:8000/deforestation_analysis?south_east_lat=24.3917701&south_east_long=60.246912&north_west_lat=24.729401&north_west_long=60.364885&season=summer' --output file.json
"""
