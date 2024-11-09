import "./Popup.css";

import placeHolderImage from "../../assets/fig2.jpg";
import { SWandNE } from "../../utilities/coordinates-helper";

type PopupProps = {
  coords: SWandNE;
};

export const Popup = ({ coords }: PopupProps) => {
  console.log("In popup");
  //   const navigate = useNavigate();

  const hanleOnClick = () => {
    const toPath = `/image?swcoord=${coords?.sw}&neCoord=${coords?.ne}`;
    console.log("toPath", toPath);
    // navigate(toPath);
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
