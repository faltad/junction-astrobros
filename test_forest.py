from datetime import datetime
import config
from packages.models import Coords, DateRange
from packages.sentinel import (
    get_oil_spill_analysis,
)


def run():
    settings = config.Settings()
    pic = get_oil_spill_analysis(
        config=settings.prepare_sh_config(),
        date_range=DateRange(
            start_date=datetime(2019, 10, 13), end_date=datetime(2019, 10, 13)
        ),
        coords=Coords(
            south_west_latitude=21.2,
            south_west_longitude=37.8,
            north_east_latitude=21.7,
            north_east_longitude=38.26,
        ),
    )
    print(str(pic))


if __name__ == "__main__":
    run()


"""
curl 'http://localhost:8000/deforestation_analysis?south_east_lat=24.3917701&south_east_long=60.246912&north_west_lat=24.729401&north_west_long=60.364885&season=summer' --output file.json
"""
