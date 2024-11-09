import { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import "@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css";
import "mapbox-gl/dist/mapbox-gl.css";
import "./Map.css";
import { Popup } from "../Popup/Popup";
import { createRoot } from "react-dom/client";
import {
  findSWandNECoordinates,
  SWandNE,
} from "../../utilities/coordinates-helper";

export const Map = () => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const [coords, setCoords] = useState({ lat: 0, lon: 0 });

  let map: mapboxgl.Map | null = null;

  const draw = new MapboxDraw({
    displayControlsDefault: false,
    controls: {
      polygon: true,
      trash: true,
    },
    defaultMode: "draw_polygon",
  });

  useEffect(() => {
    const successCallBack = (position: GeolocationPosition) => {
      console.log("POSITION", position);
      setCoords({
        lat: position.coords.latitude,
        lon: position.coords.longitude,
      });
    };

    navigator.geolocation.getCurrentPosition(successCallBack, (error) =>
      console.error(error)
    );
  }, []);

  useEffect(() => {
    if (!import.meta.env.VITE_MAPBOX_TOKEN) {
      console.error("Mapbox token is not set");
      return;
    }
    mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN;

    if (mapContainerRef.current === null) {
      return;
    }

    if (map) {
        map.off('click', addPopUp);
    }

    console.log("COORDS", coords);

    map = new mapboxgl.Map({
      container: mapContainerRef.current,
      //style: "mapbox://styles/mapbox/dark-v11",
      style: "mapbox://styles/mapbox/satellite-v9",
      center: [coords.lon, coords.lat],
      zoom: 9,
    });

    map.addControl(draw);

    map.on("draw.create", getFinalCoordinates);

    map.addControl(
      new mapboxgl.GeolocateControl({
        positionOptions: {
          enableHighAccuracy: true,
        },
        trackUserLocation: true,
        showUserHeading: true,
      })
    );

    return () => {
      if (!map) {
        return;
      }

      map.remove();
    };
  }, [coords]);

  const addPopUp = () => {
    if (!map) {
      return;
    } else {
        map.off("click", addPopUp);
    }

    const coordsData: GeoJSON.FeatureCollection = draw.getAll();

    if (coordsData.features.length !== 1) {
      return;
    }

    if (coordsData.features[0].geometry.type !== "Polygon") {
      return;
    }

    console.log(coordsData.features[0]);
    const SWNECoords = findSWandNECoordinates(
      coordsData.features[0].geometry.coordinates
    );

    const parentNode = document.createElement("div");
    const root = createRoot(parentNode);
  
    root.render(<Popup coords={SWNECoords} />);
  
    new mapboxgl.Popup({ maxWidth: "500px", anchor: "bottom-left" })
      .setLngLat([SWNECoords!.ne[0], SWNECoords!.ne[1]])
      .setDOMContent(parentNode)
      .addTo(map);
  };
  

  const getFinalCoordinates = () => {
    if (!map) {
        return;
    } else {
        map.off("click", addPopUp);
    }
    map.on("click", addPopUp);
  };

  return (
    <div
      id="map-container"
      ref={mapContainerRef}
      style={{
        position: "absolute",
        top: 32,
        bottom: 32,
        left: 0,
        overflow: "hidden",
        borderRadius: 50,
        width: "calc(100% - 24px)",
      }}
    />
  );
};
