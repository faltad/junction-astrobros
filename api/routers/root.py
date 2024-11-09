from typing import Annotated
from fastapi import APIRouter, Depends, Response

from api.dependencies import get_settings
from packages.models import Coords
from packages.sentinel import get_true_colors_sentinel2
from fastapi.responses import StreamingResponse
import config

router = APIRouter()


@router.get("/")
def root():
    return {"message": "Hello World"}


@router.get(
    "/image", responses={200: {"content": {"image/png": {}}}}, response_class=Response
)
def get_image(
    settings: Annotated[config.Settings, Depends(get_settings)], lat: float, long: float
):
    file_content = get_true_colors_sentinel2(
        config=settings.prepare_sh_config(), coords=Coords(latitude=lat, longitude=long)
    )
    # media_type here sets the media type of the actual response sent to the client.
    return StreamingResponse(
        file_content,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=example.txt"},
    )
