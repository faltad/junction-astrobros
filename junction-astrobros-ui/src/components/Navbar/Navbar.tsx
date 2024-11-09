import logo from "../../assets/logo.svg";
import dashboard from "../../assets/dashboard-icon.svg";
import analytics from "../../assets/analytics-icon.svg";
import land from "../../assets/land-icon.svg";
import doc from "../../assets/doc-icon.svg";
import "./Navbar.css";

export default function Navbar() {
  return (
    <div className="navbarWrapper">
      <div className="navbar">
        <img src={logo}></img>
        <img src={dashboard}></img>
        <img src={analytics}></img>
        <img src={land}></img>
        <img src={doc}></img>
      </div>
    </div>
  );
}
