export enum Layer {
  NDVI = "ndvi",
  TRUE_COLORS = "true_colors",
  OIL_SLICK_AND_RED_TIDE = "oil_slick_and_red_tide",
}

type LayerPickerProps = {
  setLayer: Function;
};
export const LayerPicker = ({ setLayer }: LayerPickerProps) => {
  const handleOnClick = (layer: Layer) => {
    setLayer(layer);
  };

  return (
    <div className="button-group">
      <button onClick={() => handleOnClick(Layer.NDVI)} className="button">
        NDVI
      </button>
      <button
        onClick={() => handleOnClick(Layer.TRUE_COLORS)}
        className="button"
      >
        TRUE COLORS
      </button>
      <button
        onClick={() => handleOnClick(Layer.OIL_SLICK_AND_RED_TIDE)}
        className="button"
      >
        OIL SLICK
      </button>
    </div>
  );
};
