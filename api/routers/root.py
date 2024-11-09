import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Response

from api.dependencies import get_settings
from packages.models import Coords, DateRange
from packages.sentinel import get_true_colors, get_ndvi_layer
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
    south_east_lat: float,
    south_east_long: float,
    north_west_lat: float,
    north_west_long: float,
    start_date: datetime,
    end_date: datetime,
    layer: str = "true_colors",
):
    coords = Coords(
            north_west_longitude=north_west_long,
            north_west_latitude=north_west_lat,
            south_east_longitude=south_east_long,
            south_east_latitude=south_east_lat,
    )
    date_range = DateRange(start_date, end_date)
    settings = settings.prepare_sh_config()
    if layer == "ndvi":
        file_content = get_ndvi_layer(
            config=settings,
            coords=coords,
            date_range=date_range,
        )
    else:
        file_content = get_true_colors(
            config=settings,
            coords=coords,
            date_range=date_range,
        )

    # media_type here sets the media type of the actual response sent to the client.
    return StreamingResponse(
        file_content,
        media_type="image/png",
        headers={"Content-Disposition": "attachment; filename=image.png"},
    )
