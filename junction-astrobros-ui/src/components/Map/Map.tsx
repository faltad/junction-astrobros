import { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";

import "mapbox-gl/dist/mapbox-gl.css";

import "./Map.css";

import placeHolderImg from "../../assets/placeholder-img.jpg";
import ReactDOM from "react-dom";
import { Popup } from "../Popup/Popup";

export const Map = () => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const popUpRef = useRef(new mapboxgl.Popup({ offset: 15 }));
  const [coords, setCoords] = useState({ lat: 0, lon: 0 });

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

    console.log("COORDS", coords);

    const map = new mapboxgl.Map({
      container: mapContainerRef.current,
      style: "mapbox://styles/mapbox/dark-v11",
      //style: "mapbox://styles/mapbox/satellite-v9",
      center: [coords.lon, coords.lat],
      zoom: 9,
      minZoom: 7,
      maxZoom: 11,
    });

    map.addControl(
      new mapboxgl.GeolocateControl({
        positionOptions: {
          enableHighAccuracy: true,
        },
        trackUserLocation: true,
        showUserHeading: true,
      })
    );

    map.on("click", (e) => {
      console.log("map clicked", e);

      const popupNode = document.createElement("div")
      ReactDOM.render(
        <Popup
          routeName={"Route name"}
          routeNumber={"Route number"}
          city={"City"}
          type={"Type"}
        />,
        popupNode
      )
      popUpRef.current
        .setLngLat(e.lngLat)
        .setDOMContent(popupNode)
        .addTo(map)

    //   new mapboxgl.Popup()
    //     .setLngLat(e.lngLat)
    //     .setHTML(
    //       `<h3>Coordinates</h3><p>Lng: ${e.lngLat.lng.toFixed(
    //         4
    //       )}, Lat: ${e.lngLat.lat.toFixed(
    //         4
    //       )}</p><img src=${placeHolderImg}>`
    //     )
    //     .addTo(map);
    });

    return () => {
      map.remove();
    };
  }, [coords]);

  return (
    <>
      <div id="map-container" className="map-container" ref={mapContainerRef} />
    </>
  );
};
