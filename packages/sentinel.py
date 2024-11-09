import io
from typing import Optional

import numpy as np

from packages.models import Coords


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


def plot_image(
    image: np.ndarray,
    factor: float = 1.0,
    clip_range: Optional[tuple[float, float]] = None,
    **kwargs,
) -> io.BytesIO:
    """Utility function for plotting RGB images and returning as a file-like object."""
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))

    ax.axis('off')

    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)

    ax.set_xticks([])
    ax.set_yticks([])

    # Create a BytesIO object to save the image
    img_buffer = io.BytesIO()
    # tight + 0 pad means no white border on side of pic.
    plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0)
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


def get_true_colors(coords: Coords, config: SHConfig) -> io.BytesIO:
    """Returns a file-like object with the true colors picture."""
    bbox = prepare_bbox(coords)
    size = calculate_size(bbox)
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
                #time_interval=("2024-10-23", "2024-10-24"),
                time_interval=("2023-10-14", "2023-10-26"),
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


def get_ndvi_layer(coords: Coords, config: SHConfig) -> io.BytesIO:
    """
    Normalized difference vegetation index
    The value range of the NDVI is -1 to 1. Negative values of NDVI (values approaching -1) correspond to water.
     Values close to zero (-0.1 to 0.1) generally correspond to barren areas of rock, sand, or snow.
      Low, positive values represent shrub and grassland (approximately 0.2 to 0.4), while high values indicate
      temperate and tropical rainforests (values approaching 1). It is a good proxy for live green vegetation.
    """
    bbox = prepare_bbox(coords)
    size = calculate_size(bbox)
    evalscript_true_color = """
        function setup() {
           return {
              input: ["B04", "B08", "dataMask"],
              output: { bands: 4 }
           };
        }
        
        const ramp = [
           [-0.5, 0x0c0c0c],
           [-0.2, 0xbfbfbf],
           [-0.1, 0xdbdbdb],
           [0, 0xeaeaea],
           [0.025, 0xfff9cc],
           [0.05, 0xede8b5],
           [0.075, 0xddd89b],
           [0.1, 0xccc682],
           [0.125, 0xbcb76b],
           [0.15, 0xafc160],
           [0.175, 0xa3cc59],
           [0.2, 0x91bf51],
           [0.25, 0x7fb247],
           [0.3, 0x70a33f],
           [0.35, 0x609635],
           [0.4, 0x4f892d],
           [0.45, 0x3f7c23],
           [0.5, 0x306d1c],
           [0.55, 0x216011],
           [0.6, 0x0f540a],
           [1, 0x004400],
        ];
        
        const visualizer = new ColorRampVisualizer(ramp);
        
        function evaluatePixel(samples) {
           let ndvi = index(samples.B08, samples.B04);
           let imgVals = visualizer.process(ndvi);
           return imgVals.concat(samples.dataMask)
        }
    """

    request_true_color = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C.define_from(
                    "s2l1c", service_url=config.sh_base_url
                ),
                # time_interval=("2024-10-23", "2024-10-24"),
                time_interval=("2024-10-14", "2024-10-26"),
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
    # factor 1 to not over brighten the picture
    return plot_image(image, factor=1 / 255, clip_range=(0, 1))
