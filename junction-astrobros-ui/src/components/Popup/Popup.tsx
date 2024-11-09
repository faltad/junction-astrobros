import './Popup.css';

export const Popup = ({ routeName, routeNumber, city, type }: any) => (
    <div className="popup">
      <h3 className="route-name">{routeName}</h3>
      <div className="route-metric-row">
        <h4 className="row-title">Route #</h4>
        <div className="row-value">{routeNumber}</div>
      </div>
      <div className="route-metric-row">
        <h4 className="row-title">Route Type</h4>
        <div className="row-value">{type}</div>
      </div>
      <p className="route-city">Serves {city}</p>
    </div>
  )