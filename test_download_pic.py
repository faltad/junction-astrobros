# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///
from datetime import datetime


from packages.models import Coords, DateRange
from packages.sentinel import get_true_colors, get_ndvi_layer

from config import Settings


def main():
    config = Settings().prepare_sh_config()

    betsiboka_coords = Coords(latitude=46.16, longitude=-16.15)
    random_helsinki_coords = Coords(latitude=24.846971, longitude=60.173445)
    colombia_coords = Coords(latitude=-75.000761, longitude=3.703350)
    coords = colombia_coords
    daterange = DateRange(
        start_date=datetime(2024, 10, 12), end_date=datetime(2024, 10, 15)
    )
    pic = get_true_colors(coords, daterange, config)
    with open("output_image.png", "wb") as f:
        f.write(pic.getvalue())
    pic = get_ndvi_layer(coords, daterange, config)
    with open("image_ndvi.png", "wb") as f:
        f.write(pic.getvalue())


if __name__ == "__main__":
    main()
