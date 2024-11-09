import './Layout.css';
import { Map } from '../Map/Map';

export const Layout = () => {
    return (
        <div className="app">
          <div className="sidebar">astrobors</div>
          <div className="mapWrapper">
            <Map />
          </div>
        </div>
      );
}