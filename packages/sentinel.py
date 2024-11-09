import io
from typing import Optional

import numpy as np

from packages.models import Coords, DateRange


import logging
import matplotlib.pyplot as plt

from sentinelhub import (
    SHConfig,
    CRS,
    BBox,
    DataCollection,
    MimeType,
    SentinelHubRequest,
    bbox_to_dimensions,
)


logger = logging.getLogger(__name__)

DATEFORMAT = "%Y-%m-%d"


def plot_image(
    image: np.ndarray,
    factor: float = 1.0,
    clip_range: Optional[tuple[float, float]] = None,
    **kwargs,
) -> io.BytesIO:
    """Utility function for plotting RGB images and returning as a file-like object."""
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))

    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)

    ax.set_xticks([])
    ax.set_yticks([])

    # Create a BytesIO object to save the image
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    img_buffer.seek(0)  # Reset the file pointer to the start of the buffer

    # Close the figure to free memory
    plt.close(fig)

    return img_buffer


def prepare_bbox(coords: Coords) -> BBox:
    # hardcoded bounding box for now
    bbox_size = (0.35, 0.35)
    coords_wgs84 = (
        coords.latitude,
        coords.longitude,
        coords.latitude + bbox_size[0],
        coords.longitude + bbox_size[1],
    )
    return BBox(bbox=coords_wgs84, crs=CRS.WGS84)


def calculate_size(bbox: BBox) -> tuple[int, int]:
    """width and height in pixels for given bounding box and pixel resolution"""
    # hardcoded for now, we need to calculate that based on given size of bbox
    resolution = 20
    size = bbox_to_dimensions(bbox, resolution=resolution)

    logger.info(f"Image shape at {resolution}m resolution: {size} pixels")
    return size


def get_true_colors_sentinel2(
    coords: Coords, date_range: DateRange, config: SHConfig
) -> io.BytesIO:
    """Returns a file-like object with the true colors picture."""
    bbox = prepare_bbox(coords)
    size = calculate_size(bbox)
    start_date = date_range.start_date.strftime(DATEFORMAT)
    end_date = date_range.end_date.strftime(DATEFORMAT)

    evalscript_true_color = """
            //VERSION=3

            function setup() {
                return {
                    input: [{
                        bands: ["B02", "B03", "B04"]
                    }],
                    output: {
                        bands: 3
                    }
                };
            }

            function evaluatePixel(sample) {
                return [sample.B04, sample.B03, sample.B02];
            }
        """

    request_true_color = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C.define_from(
                    "s2l1c", service_url=config.sh_base_url
                ),
                time_interval=(start_date, end_date),
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=bbox,
        size=size,
        config=config,
    )
    true_color_imgs = request_true_color.get_data()
    image = true_color_imgs[0]

    # plot function
    # factor 1/255 to scale between 0-1
    # factor 3.5 to increase brightness
    return plot_image(image, factor=3.5 / 255, clip_range=(0, 1))
