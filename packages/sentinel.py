from datetime import datetime
from enum import Enum
import io
from typing import Optional
import xarray as xr
import numpy as np

from packages import exceptions
from packages.models import Coords, DateRange, Seasons

from ipyleaflet import GeoJSON, Map, basemaps

from pathlib import Path
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
    SentinelHubDownloadClient,
)
import sentinelhub

logger = logging.getLogger(__name__)

DATEFORMAT = "%Y-%m-%d"


class AvailableLayers(str, Enum):
    NDVI = "ndvi"
    TRUE_COLORS = "true_colors"


def plot_image(
    image: np.ndarray,
    factor: float = 1.0,
    clip_range: Optional[tuple[float, float]] = None,
    **kwargs,
) -> io.BytesIO:
    """Utility function for plotting RGB images and returning as a file-like object."""
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))

    ax.axis("off")

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

    coords_wgs84 = (
        coords.south_east_latitude,
        coords.south_east_longitude,
        coords.north_west_latitude,
        coords.north_west_longitude,
    )
    return BBox(bbox=coords_wgs84, crs=CRS.WGS84)


def calculate_size(bbox: BBox) -> tuple[int, int]:
    """width and height in pixels for given bounding box and pixel resolution"""
    # hardcoded for now, we need to calculate that based on given size of bbox
    resolution = 20
    size = bbox_to_dimensions(bbox, resolution=resolution)

    # TODO: error handling if size too big
    logger.info(f"Image shape at {resolution}m resolution: {size} pixels")
    return size


def _make_sentinel_request(
    date_range: DateRange, evalscript: str, config: SHConfig, coords: Coords
):
    bbox = prepare_bbox(coords)
    size = calculate_size(bbox)
    start_date = date_range.start_date.strftime(DATEFORMAT)
    end_date = date_range.end_date.strftime(DATEFORMAT)
    r = SentinelHubRequest(
        evalscript=evalscript,
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
    imgs = r.get_data()
    # TODO: beware of no pictures and so on. This works only in case we want to show most recent
    image = imgs[0]
    return image


def get_true_colors(
    coords: Coords, date_range: DateRange, config: SHConfig
) -> io.BytesIO:
    """Returns a file-like object with the true colors picture."""

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

    image = _make_sentinel_request(date_range, evalscript_true_color, config, coords)

    # plot function
    # factor 1/255 to scale between 0-1
    # factor 3.5 to increase brightness
    return plot_image(image, factor=3.5 / 255, clip_range=(0, 1))


def get_ndvi_layer(
    coords: Coords, date_range: DateRange, config: SHConfig
) -> io.BytesIO:
    """
    Normalized difference vegetation index
    The value range of the NDVI is -1 to 1. Negative values of NDVI (values approaching -1) correspond to water.
     Values close to zero (-0.1 to 0.1) generally correspond to barren areas of rock, sand, or snow.
      Low, positive values represent shrub and grassland (approximately 0.2 to 0.4), while high values indicate
      temperate and tropical rainforests (values approaching 1). It is a good proxy for live green vegetation.
    """
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
    try:
        image = _make_sentinel_request(
            date_range, evalscript_true_color, config, coords
        )
    except sentinelhub.exceptions.DownloadFailedException:
        raise exceptions.SentinelError()

    # plot function
    # factor 1/255 to scale between 0-1
    # factor 1 to not over brighten the picture
    return plot_image(image, factor=1 / 255, clip_range=(0, 1))


def get_bbox_forestation_analysis(coords: Coords) -> BBox:
    coords = (
        coords.south_east_latitude,
        coords.south_east_longitude,
        coords.north_west_latitude,
        coords.north_west_longitude,
    )
    epsg = 3035
    # Convert to 3035 to get crs with meters as units
    bbox = BBox(coords, CRS.WGS84).transform(CRS(epsg))

    x, y = bbox.transform(CRS.WGS84).middle

    overview_map = Map(basemap=basemaps.OpenStreetMap.Mapnik, center=(y, x), zoom=10)
    # Add geojson data
    geo_json = GeoJSON(data=bbox.transform(CRS.WGS84).geojson)
    overview_map.add_layer(geo_json)
    return bbox


def get_forestation_eval_script():
    return """
    //VERSION=3
    function setup() {
        return {
            input: ["B08", "B04", "B03", "B02", "SCL"],
            output: {
                bands: 4,
                sampleType: "INT16"
            },
            mosaicking: "ORBIT"
        }
    }

    function getFirstQuartileValue(values) {
        values.sort((a,b) => a-b);
        return getFirstQuartile(values);
    }

    function getFirstQuartile(sortedValues) {
        var index = Math.floor(sortedValues.length / 4);
        return sortedValues[index];
    }

    function validate(sample) {
        // Define codes as invalid:
        const invalid = [
            0, // NO_DATA
            1, // SATURATED_DEFECTIVE
            3, // CLOUD_SHADOW
            7, // CLOUD_LOW_PROBA
            8, // CLOUD_MEDIUM_PROBA
            9, // CLOUD_HIGH_PROBA
            10 // THIN_CIRRUS
        ]
        return !invalid.includes(sample.SCL)
    }

    function evaluatePixel(samples) {
        var valid = samples.filter(validate);
        if (valid.length > 0 ) {
            let cloudless = {
                b08: getFirstQuartileValue(valid.map(s => s.B08)),
                b04: getFirstQuartileValue(valid.map(s => s.B04)),
                b03: getFirstQuartileValue(valid.map(s => s.B03)),
                b02: getFirstQuartileValue(valid.map(s => s.B02)),
            }
            let ndvi = ((cloudless.b08 - cloudless.b04) / (cloudless.b08 + cloudless.b04))
            // This applies a scale factor so the data can be saved as an int
            let scale = [cloudless.b04, cloudless.b03, cloudless.b02, ndvi].map(v => v*10000);
            return scale
        }
        // If there isn't enough data, return NODATA
        return [-32768, -32768, -32768, -32768]
    }
    """


def get_interval_of_interest(season: Seasons, year: int) -> tuple[datetime, datetime]:
    match season:
        case Seasons.SUMMER:
            return datetime(year, 6, 1), datetime(year, 9, 1)
        case Seasons.AUTUMN:
            return datetime(year, 9, 1), datetime(year, 11, 1)
        case Seasons.SPRING:
            return datetime(year, 3, 1), datetime(year, 6, 1)
        case Seasons.WINTER:
            return datetime(year, 1, 1), datetime(year, 3, 1)
        case _:
            return datetime(year, 6, 1), datetime(year, 9, 1)


def get_forestation_analysis(config: SHConfig, season: Seasons, coords: Coords):
    bbox = get_bbox_forestation_analysis(coords)

    resolution = (100, 100)

    def get_request(year, config: SHConfig):
        time_interval = get_interval_of_interest(season=season, year=year)
        return SentinelHubRequest(
            evalscript=get_forestation_eval_script(),
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L2A.define_from(
                        "s2", service_url=config.sh_base_url
                    ),
                    time_interval=time_interval,
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
            bbox=bbox,
            resolution=resolution,
            config=config,
            data_folder="./data",
        )

    # create a dictionary of requests
    sh_requests = {}
    for year in range(2019, 2025):
        sh_requests[year] = get_request(year, config)

    list_of_requests = [request.download_list[0] for request in sh_requests.values()]

    # download data with multiple threads
    SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=7)

    def request_output_path(request):
        # Gets the full path to the output from a request
        return Path(request.data_folder, request.get_filename_list()[0])

    for year, request in sh_requests.items():
        request_output_path(request).rename(f"./data/{year}.tif")


def process_forest_data_generate_deforestation_rate_graph() -> io.BytesIO:
    def add_time_dim(xda):
        # This pre-processes the file to add the correct
        # year from the filename as the time dimension
        year = int(Path(xda.encoding["source"]).stem)
        return xda.expand_dims(year=[year])

    resolution = (100, 100)
    tiff_paths = Path("./data").glob("*.tif")
    ds_s2 = xr.open_mfdataset(
        tiff_paths,
        engine="rasterio",
        preprocess=add_time_dim,
        band_as_variable=True,
    )
    ds_s2 = ds_s2.rename(
        {
            "band_1": "R",
            "band_2": "G",
            "band_3": "B",
            "band_4": "NDVI",
        }
    )
    ds_s2 = ds_s2 / 10000

    def to_km2(dataarray, resolution):
        # Calculate forest area
        return dataarray * np.prod(list(resolution)) / 1e6

    # analysis
    ds_s2["FOREST"] = ds_s2.NDVI > 0.7
    forest_pixels = ds_s2.FOREST.sum(["x", "y"])
    forest_area_km2 = to_km2(forest_pixels, resolution)
    forest_area_km2.plot()
    plt.title("Forest Cover")
    plt.ylabel("Forest Cover [km²]")
    plt.ylim(0)

    # Create a BytesIO object to save the image
    img_buffer = io.BytesIO()
    # tight + 0 pad means no white border on side of pic.
    plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0)
    img_buffer.seek(0)  # Reset the file pointer to the start of the buffer
    return img_buffer


def process_forest_data_generate_visualisation() -> dict[str, io.BytesIO]:
    def add_time_dim(xda):
        # This pre-processes the file to add the correct
        # year from the filename as the time dimension
        year = int(Path(xda.encoding["source"]).stem)
        return xda.expand_dims(year=[year])

    files = {}
    tiff_paths = Path("./data").glob("*.tif")
    for path in tiff_paths:
        ds_s2 = xr.open_mfdataset(
            path,
            engine="rasterio",
            preprocess=add_time_dim,
            band_as_variable=True,
        )
        ds_s2 = ds_s2.rename(
            {
                "band_1": "R",
                "band_2": "G",
                "band_3": "B",
                "band_4": "NDVI",
            }
        )
        ds_s2 = ds_s2 / 10000

        # # vizualisation
        ds_s2.NDVI.plot(cmap="PRGn", x="x", y="y", col="year", col_wrap=1)

        plt.axis("off")

        for ax in plt.gcf().axes:
            ax.set_title("")
        # Create a BytesIO object to save the image
        img_buffer = io.BytesIO()
        # tight + 0 pad means no white border on side of pic.
        plt.savefig(img_buffer, format="png", bbox_inches="tight", pad_inches=0)
        img_buffer.seek(0)  # Reset the file pointer to the start of the buffer
        files[f"{path.stem}"] = img_buffer

    return files


def get_sentinel_image(
    layer: AvailableLayers, coords: Coords, date_range: DateRange, config: SHConfig
) -> io.BytesIO:
    if layer == AvailableLayers.TRUE_COLORS:
        return get_true_colors(coords, date_range, config)
    elif layer == AvailableLayers.NDVI:
        return get_ndvi_layer(coords, date_range, config)
    raise ValueError(f"Unavailable layer {str(layer.value)}")
