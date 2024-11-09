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
import { useNavigate } from "react-router-dom";

export const Map = () => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const [coords, setCoords] = useState({ lat: 0, lon: 0 });
  const [coordsToQuery, setCoordsToQuery] = useState<SWandNE>(null);

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

  const draw = new MapboxDraw({
    displayControlsDefault: false,
    controls: {
      polygon: true,
      trash: true,
    },
    defaultMode: "draw_polygon",
  });

  const getFinalCoordinates = () => {
    const coordsData: GeoJSON.FeatureCollection = draw.getAll();
    if (coordsData.features.length === 1) {
      if (coordsData.features[0].geometry.type === "Polygon") {
        setCoordsToQuery(
          findSWandNECoordinates(coordsData.features[0].geometry.coordinates)
        );
      }
    }
  };

  useEffect(() => {
    if (!import.meta.env.VITE_MAPBOX_TOKEN) {
      console.error("Mapbox token is not set");
      return;
    }
    mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN;

    if (mapContainerRef.current === null) {
      return;
    }

    console.log("COORDS", coords);

    const map = new mapboxgl.Map({
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
      map.remove();
    };
  }, [coords]);

  console.log(coordsToQuery);

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
