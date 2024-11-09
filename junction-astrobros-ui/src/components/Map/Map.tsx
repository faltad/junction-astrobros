import { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";

export const Map = () => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
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
      center: [coords.lon, coords.lat],
      zoom: 9,
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

    return () => {
      map.remove();
    };
  }, [coords]);

  return (
    <div
      id="map-container"
      ref={mapContainerRef}
      style={{
        position: "absolute",
        top: 32,
        bottom: 32,
        right: 24,
        overflow: "hidden",
        borderRadius: 50,
        width: "100%",
      }}
    />
  );
};
