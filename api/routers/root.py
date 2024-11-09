import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Response

from api.dependencies import get_settings
from packages.models import Coords, DateRange, Seasons
from packages.sentinel import (
    get_forestation_analysis,
    get_true_colors,
    process_forest_data_generate_visualisation,
)
from fastapi.responses import StreamingResponse
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
    lat: float,
    long: float,
    start_date: datetime,
    end_date: datetime,
):
    file_content = get_true_colors(
        config=settings.prepare_sh_config(),
        coords=Coords(latitude=lat, longitude=long),
        date_range=DateRange(start_date, end_date),
    )
    # media_type here sets the media type of the actual response sent to the client.
    return StreamingResponse(
        file_content,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=image.png"},
    )


@router.get(
    "/deforestation_analysis",
    responses={200: {"content": {"multipart/mixed": {}}}},
    response_class=Response,
)
async def send_deforestation_analysis(
    settings: Annotated[config.Settings, Depends(get_settings)],
    lat: float,
    long: float,
    season: Seasons,
):
    # Paths to your image files
    get_forestation_analysis(
        settings.prepare_sh_config(),
        season=Seasons.SUMMER,
        coords=Coords(latitude=1, longitude=1),  # not used at the moment
    )

    # Prepare the multipart response
    boundary = "image-boundary"
    response = Response()
    response.headers["Content-Type"] = f"multipart/mixed; boundary={boundary}"

    image_content = process_forest_data_generate_visualisation()

    return StreamingResponse(
        image_content,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=image.png"},
    )
