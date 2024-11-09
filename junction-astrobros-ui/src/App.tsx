import { Map } from "./components/Map/Map";
import "./App.css";
import Navbar from "./components/Navbar/Navbar";

function App() {
  return (
    <div className="app">
      <Navbar />
      <div className="mapWrapper">
        <Map />
      </div>
    </div>
  );
}

export default App;
