import logging
from typing import Annotated
from fastapi import APIRouter, Depends, Response

from api.dependencies import get_settings
from packages.models import Coords, DateRange
from packages.sentinel import get_true_colors_sentinel2
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
    file_content = get_true_colors_sentinel2(
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
