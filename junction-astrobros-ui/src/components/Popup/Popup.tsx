import "./Popup.css";

import placeHolderImage from "../../assets/fig2.jpg";

type PopupProps = {
  swCoord: string;
  neCoord: string;
};

export const Popup = ({ swCoord, neCoord }: PopupProps) => {
  //   const navigate = useNavigate();

  const hanleOnClick = () => {
    const toPath = `/image?swcoord=${swCoord}&neCoord=${neCoord}`;
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
