import { Suspense } from "react";
import {
  Await,
  defer,
  LoaderFunctionArgs,
  useLoaderData,
} from "react-router-dom";
import "./DetailedPage.css";

interface FetchImageParams {
  southWestLat: string;
  southWestLong: string;
  northEastLat: string;
  northEastLong: string;
}

export const imagesPromise = async ({
  southWestLat,
  southWestLong,
  northEastLat,
  northEastLong,
}: FetchImageParams) => {
  const url = new URL("http://172.20.10.3:8000/deforestation_analysis");

  // Set query parameters
  url.searchParams.append("south_west_lat", southWestLat.toString());
  url.searchParams.append("south_west_long", southWestLong.toString());
  url.searchParams.append("north_east_lat", northEastLat.toString());
  url.searchParams.append("north_east_long", northEastLong.toString());
  url.searchParams.append("season", "summer");

  try {
    const response = await fetch(url.pathname + url.search, {
      method: "GET",
      headers: {
        "Content-Type": "multipart/mixed",
      },
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json(); // Parse as JSON
    console.log("DATA", data);
    return data;
  } catch (error) {
    console.error("Failed to fetch image:", error);
    throw error;
  }
};

export const loader = ({ request }: LoaderFunctionArgs) => {
  const urlObj = new URL(request.url);

  const southWestLat: string = urlObj.searchParams.get("swlat")!;
  const southWestLong: string = urlObj.searchParams.get("swlon")!;
  const northEastLat: string = urlObj.searchParams.get("nelat")!;
  const northEastLong: string = urlObj.searchParams.get("nelon")!;

  console.log(southWestLat, southWestLong, northEastLat, northEastLong);

  return defer({
    imagePromise: imagesPromise({
      southWestLat,
      southWestLong,
      northEastLat,
      northEastLong,
    }),
  });
};

export const DetailPage = () => {
  const loaderData = useLoaderData() as { imagePromise: unknown };
  console.log(loaderData);
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Await
        resolve={loaderData.imagePromise}
        errorElement={<div>Something went wrong while fetching data...</div>}
      >
        {(images) => (
          <>
            <div className="title">Deforestation data</div>
            <div className="container">
              {Object.keys(images).map((imageYear) => {
                if (imageYear !== "graph") {
                  return (
                    <div className="image-item">
                      <img src={`data:image/png;base64,${images[imageYear]}`} />
                      <p className="caption">Year: {imageYear}</p>
                    </div>
                  );
                }
              })}
            </div>
          </>
        )}
      </Await>
    </Suspense>
  );
};
