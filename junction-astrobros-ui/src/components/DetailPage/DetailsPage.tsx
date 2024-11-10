import { Suspense } from "react";
import {
  Await,
  defer,
  LoaderFunctionArgs,
  useLoaderData,
  useNavigation,
} from "react-router-dom";
import "./DetailedPage.css";
import Spinner from "../LoadingSpinner/LoadingSpinner";
import { ButtonGroup } from "../ButtonGroup/ButtonGroup";

export type Season = "winter" | "spring" | "summer" | "autumn";

interface FetchImageParams {
  southWestLat: string;
  southWestLong: string;
  northEastLat: string;
  northEastLong: string;
  season: Season;
}

export const imagesPromise = async ({
  southWestLat,
  southWestLong,
  northEastLat,
  northEastLong,
  season,
}: FetchImageParams) => {
  const url = new URL("http://172.20.10.3:8000/deforestation_analysis");

  // Set query parameters
  url.searchParams.append("south_west_lat", southWestLat.toString());
  url.searchParams.append("south_west_long", southWestLong.toString());
  url.searchParams.append("north_east_lat", northEastLat.toString());
  url.searchParams.append("north_east_long", northEastLong.toString());
  url.searchParams.append("season", season);

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
  const season: Season =
    (urlObj.searchParams.get("season") as Season) || "spring";

  console.log(southWestLat, southWestLong, northEastLat, northEastLong, season);

  return defer({
    imagePromise: imagesPromise({
      southWestLat,
      southWestLong,
      northEastLat,
      northEastLong,
      season,
    }),
  });
};

export const DetailPage = () => {
  const loaderData = useLoaderData() as { imagePromise: unknown };
  const navigation = useNavigation();
  return (
    <>
      <Suspense
        fallback={
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              height: "100%",
            }}
          >
            <Spinner />
          </div>
        }
      >
        <Await
          resolve={loaderData.imagePromise}
          errorElement={<div>Something went wrong while fetching data...</div>}
        >
          {(images) => (
            <>
              {navigation.state === "loading" ? (
                <div
                  style={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    height: "100%",
                  }}
                >
                  <Spinner />
                </div>
              ) : (
                <>
                  <div className="button-group-container">
                    <div className="title">Forest cover changes</div>
                    <ButtonGroup />
                  </div>
                  <br />
                  <div className="container">
                    {Object.keys(images).map((imageYear) => {
                      if (imageYear !== "graph") {
                        return (
                          <div className="image-item" key={`${imageYear}`}>
                            <img
                              src={`data:image/png;base64,${images[imageYear]}`}
                            />
                            <p className="caption">Year: {imageYear}</p>
                          </div>
                        );
                      }
                    })}
                  </div>
                  <div className="info-container">
                    {Object.keys(images).map((imageYear) => {
                      if (imageYear === "graph") {
                        return (
                          <div className="image-item">
                            <img
                              src={`data:image/png;base64,${images[imageYear]}`}
                            />
                          </div>
                        );
                      }
                    })}
                    <div className="gradient-container">
                      <div className="gradient-labels-container">
                        <div className="gradient-prgn"></div>
                        <div className="labels">
                          <span>1</span>
                          <span>-1</span>
                        </div>
                      </div>
                      <p>
                        NDVI is a simple, but effective index for quantifying
                        green vegetation. It normalizes green leaf scattering in
                        Near Infra-red wavelengths with chlorophyll absorption
                        in red wavelengths.
                        <br />
                        <br />
                        The value range of the NDVI is -1 to 1. Negative values
                        of NDVI (values approaching -1) correspond to water.
                        Values close to zero (-0.1 to 0.1) generally correspond
                        to barren areas of rock, sand, or snow. Low, positive
                        values represent shrub and grassland (approximately 0.2
                        to 0.4), while high values indicate temperate and
                        tropical rainforests (values approaching 1)
                      </p>
                    </div>
                  </div>
                </>
              )}
            </>
          )}
        </Await>
      </Suspense>
    </>
  );
};
