import "./Popup.css";
import { SWandNE } from "../../utilities/coordinates-helper";
import { useEffect, useState } from "react";
import Spinner from "../LoadingSpinner/LoadingSpinner";

type PopupProps = {
  coords: SWandNE;
};

interface FetchImageParams {
  southWestLat: number;
  southWestLong: number;
  northEastLat: number;
  northEastLong: number;
  startDate: string; // ISO date format string
  endDate: string; // ISO date format string
  layer?: string; // Optional, defaults to "true_colors"
}

async function fetchImage({
  southWestLat,
  southWestLong,
  northEastLat,
  northEastLong,
  startDate,
  endDate,
  layer = "true_colors", // Default to "true_colors" if not provided
}: FetchImageParams) {
  const url = new URL("http://10.87.1.83:8000/image");

  // Set query parameters
  url.searchParams.append("south_west_lat", southWestLat.toString());
  url.searchParams.append("south_west_long", southWestLong.toString());
  url.searchParams.append("north_east_lat", northEastLat.toString());
  url.searchParams.append("north_east_long", northEastLong.toString());
  url.searchParams.append("start_date", startDate);
  url.searchParams.append("end_date", endDate);
  url.searchParams.append("layer", layer);

  try {
    const response = await fetch(url.pathname + url.search, {
      method: "GET",
      headers: {
        "Content-Type": "image/png",
      },
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`);
    }

    const data = await response.blob(); // Parse as JSON
    console.log(data);
    return data;
  } catch (error) {
    console.error("Failed to fetch image:", error);
    throw error;
  }
}

export const Popup = ({ coords }: PopupProps) => {
  const [img, setImg] = useState<string>("");
  console.log("In popup");
  //   const navigate = useNavigate();

  const hanleOnClick = () => {
    const toPath = `/image?swcoord=${coords?.sw}&neCoord=${coords?.ne}`;
    console.log("toPath", toPath);
    // navigate(toPath);
  };

  useEffect(() => {
    fetchImage({
      southWestLat: coords!.sw[1],
      southWestLong: coords!.sw[0],
      northEastLat: coords!.ne[1],
      northEastLong: coords!.ne[0],
      startDate: "2023-01-01",
      endDate: "2023-01-07",
      layer: "ndvi",
    })
      .then((data) => setImg(URL.createObjectURL(data)))
      .finally(() => {
        console.log(img);
      });
  }, []);

  return (
    <div className="popup">
      {img && <img src={img} />}
      {!img && <Spinner />}
      <button onClick={hanleOnClick} className="popup-button">
        Get more details
      </button>
    </div>
  );
};
