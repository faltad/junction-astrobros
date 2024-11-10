# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///
from datetime import datetime
from random import random


from packages.models import Coords, DateRange
from packages.sentinel import get_true_colors, get_ndvi_layer

from config import Settings


def main():
    config = Settings().prepare_sh_config()

    betsiboka_coords = Coords(
        south_west_latitude=46.16,
        south_west_longitude=-16.15,
        north_east_latitude=46.51,
        north_east_longitude=-15.79,
    )
    random_helsinki_coords = Coords(
        south_west_latitude=24.795581,
        south_west_longitude=60.138594,
        north_east_latitude=25.033369,
        north_east_longitude=60.229115,
    )

    colombia_coords = Coords(
        south_west_latitude=-72.639688,
        south_west_longitude=1.792517,
        north_east_latitude=-72.598106,
        north_east_longitude=1.820838,
    )
    coords = random_helsinki_coords
    daterange = DateRange(
        start_date=datetime(2024, 9, 12), end_date=datetime(2024, 9, 21)
    )
    pic = get_true_colors(coords, daterange, config)
    with open("../output_image.png", "wb") as f:
        f.write(pic.getvalue())
    pic = get_ndvi_layer(coords, daterange, config)
    with open("../image_ndvi.png", "wb") as f:
        f.write(pic.getvalue())


if __name__ == "__main__":
    main()
    if len(sys.argv) < 3:
        print("Please run script with id + password as argument")
    else:
        main(sys.argv[1], sys.argv[2])
    if len(sys.argv) < 3:
        print("Please run script with id + password as argument")
    else:
        main(sys.argv[1], sys.argv[2])
