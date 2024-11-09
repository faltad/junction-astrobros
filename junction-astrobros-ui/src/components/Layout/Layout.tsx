import "./Layout.css";
import { Map } from "../Map/Map";
import Navbar from "../Navbar/Navbar";

export const Layout = () => {
  return (
    <div className="app">
      <Navbar />
      <div className="mapWrapper">
        <Map />
      </div>
    </div>
  );
};
