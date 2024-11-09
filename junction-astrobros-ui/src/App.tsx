import { Map } from "./components/Map/Map";
import "./App.css";

function App() {
  return (
    <div className="app">
      <div className="sidebar">astrobors</div>
      <div className="mapWrapper">
        <Map />
      </div>
    </div>
  );
}

export default App;
