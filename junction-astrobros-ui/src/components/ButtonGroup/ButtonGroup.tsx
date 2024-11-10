import { useSearchParams } from "react-router-dom";
import "./ButtonGroup.css";
import { Season } from "../DetailPage/DetailsPage";

export const ButtonGroup = () => {
  const [searchParams, setSearchParams] = useSearchParams({ season: "spring" });
  console.log("searchParams", searchParams);

  const handleOnClick = (season: Season) => {
    if (!searchParams.get("season")) {
        setSearchParams({ season });
      return;
    }
    searchParams.set("season", season);
    setSearchParams(searchParams);
  }

  return (
    <div className="button-group">
      <button
        onClick={() => handleOnClick('winter')}
        className="button"
      >
        Winter
      </button>
      <button
        onClick={() => handleOnClick('spring')}
        className="button"
      >
        Spring
      </button>
      <button
        onClick={() => handleOnClick('summer')}
        className="button"
      >
        Summer
      </button>
      <button
        onClick={() => handleOnClick('autumn')}
        className="button"
      >
        Autumn
      </button>
    </div>
  );
};
