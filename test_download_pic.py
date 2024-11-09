# /// script
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///
import sys


# Your client credentials
# client_id = '<client_id>'
# client_secret = '<secret>'

# Create a session
# client = BackendApplicationClient(client_id=client_id)
# oauth = OAuth2Session(client=client)

# Get token for the session
# token = oauth.fetch_token(token_url='https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token',
#                          client_secret=client_secret, include_client_id=True)

# All requests using this session will have an access token automatically added
# resp = oauth.get("https://sh.dataspace.copernicus.eu/configuration/v1/wms/instances")
# print(resp.content)

from typing import Any, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np

from sentinelhub import SHConfig

from packages.models import Coords
from packages.sentinel import get_true_colors_sentinel2

def prepare_config(client_id: str, client_secret: str) -> SHConfig:
    config = SHConfig()
    config.sh_client_id = client_id
    config.sh_client_secret = client_secret
    config.sh_token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    config.sh_base_url = "https://sh.dataspace.copernicus.eu"
    config.save("cdse")
    return config


def main(client_id: str, secret: str):
    config = prepare_config(client_id, secret)

    betsiboka_coords = Coords(latitude=46.16, longitude=-16.15)
    random_helsinki_coords = Coords(latitude=24.846971, longitude=60.173445)
    pic = get_true_colors_sentinel2(random_helsinki_coords, config)
    with open("output_image.png", "wb") as f:
        f.write(pic.getvalue())


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please run script with id + password as argument")
    else:
        main(sys.argv[1], sys.argv[2])