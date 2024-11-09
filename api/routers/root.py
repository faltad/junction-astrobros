import base64
import logging
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Response, HTTPException

from api.dependencies import get_settings
from packages import exceptions
from packages.models import Coords, DateRange, Seasons
from packages.sentinel import (
    get_forestation_analysis,
    process_forest_data_generate_deforestation_rate_graph,
    process_forest_data_generate_visualisation,
)
from packages.sentinel import AvailableLayers, get_sentinel_image
from fastapi.responses import JSONResponse, StreamingResponse
import config
from datetime import datetime

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/")
def root():
    return {"message": "Api sure is running"}


@router.get(
    "/image", responses={200: {"content": {"image/png": {}}}}, response_class=Response
)
async def get_image(
    settings: Annotated[config.Settings, Depends(get_settings)],
    south_east_lat: float,
    south_east_long: float,
    north_west_lat: float,
    north_west_long: float,
    start_date: datetime,
    end_date: datetime,
    layer: AvailableLayers = AvailableLayers.TRUE_COLORS,
):
    coords = Coords(
        north_west_longitude=north_west_long,
        north_west_latitude=north_west_lat,
        south_east_longitude=south_east_long,
        south_east_latitude=south_east_lat,
    )
    date_range = DateRange(start_date, end_date)
    settings = settings.prepare_sh_config()
    try:
        file_content = get_sentinel_image(layer, coords, date_range, settings)
    except exceptions.SentinelError:
        # a bit .... heavy handed but this is a hackaton
        raise HTTPException(
            status_code=400, detail="Area wrong or too big, try reducing the area."
        )

    # media_type here sets the media type of the actual response sent to the client.
    return StreamingResponse(
        file_content,
        media_type="image/png",
    )


def encode_image_to_base64(image_path: Path):
    with open(str(image_path), "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


@router.get(
    "/deforestation_analysis",
    responses={200: {"content": {"multipart/mixed": {}}}},
    response_class=Response,
)
async def send_deforestation_analysis(
    settings: Annotated[config.Settings, Depends(get_settings)],
    south_east_lat: float,
    south_east_long: float,
    north_west_lat: float,
    north_west_long: float,
    season: Seasons,
):
    coords = Coords(
        north_west_longitude=north_west_long,
        north_west_latitude=north_west_lat,
        south_east_longitude=south_east_long,
        south_east_latitude=south_east_lat,
    )
    get_forestation_analysis(settings.prepare_sh_config(), season=season, coords=coords)

    boundary = "image-boundary"
    response = Response()
    response.headers["Content-Type"] = f"multipart/mixed; boundary={boundary}"

    viz = process_forest_data_generate_visualisation()
    content = {}

    for name, img_data in viz.items():
        content[name] = base64.b64encode(img_data.read()).decode("utf-8")

    graph = process_forest_data_generate_deforestation_rate_graph()
    content["graph"] = base64.b64encode(graph.read()).decode("utf-8")

    # Return as JSON response
    return JSONResponse(content=content)
