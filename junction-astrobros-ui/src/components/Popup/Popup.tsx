import "./Popup.css";

import placeHolderImage from "../../assets/fig2.jpg";
import { NavigateFunction } from "react-router-dom";

type PopupProps = {
  swCoord: string;
  neCoord: string;
  navigate: NavigateFunction;
};

export const Popup = ({ swCoord, neCoord, navigate }: PopupProps) => {

  const hanleOnClick = () => {
    const toPath = `/map/details?swcoord=${swCoord}&neCoord=${neCoord}`;
    navigate(toPath);
  };

  return (
    <div className="popup">
      <img className="popup-image" src={placeHolderImage} />
      <button onClick={hanleOnClick} className="popup-button">
        Get more details
      </button>
    </div>
  );
};
