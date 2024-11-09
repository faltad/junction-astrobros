import "./Layout.css";
import Navbar from "../Navbar/Navbar";
import { Outlet } from "react-router-dom";

export const Layout = () => {
  return (
    <div className="app">
      <Navbar />
      <div className="mapWrapper">
        <Outlet />
      </div>
    </div>
  );
};
