import { useSearchParams } from "react-router-dom";
import "./ButtonGroup.css";

export const ButtonGroup = () => {
  const [, setSearchParams] = useSearchParams({ season: "spring" });

  return (
    <div className="button-group">
      <button
        onClick={() => setSearchParams({ season: "winter" })}
        className="button"
      >
        Winter
      </button>
      <button
        onClick={() => setSearchParams({ season: "spring" })}
        className="button active"
      >
        Spring
      </button>
      <button
        onClick={() => setSearchParams({ season: "summer" })}
        className="button"
      >
        Summer
      </button>
      <button
        onClick={() => setSearchParams({ season: "winter" })}
        className="button"
      >
        Winter
      </button>
    </div>
  );
};
