import React, { useState } from "react";
import { startOfWeek, endOfWeek, addWeeks, subWeeks, format } from "date-fns";

type WeekPickerProps = {
  date: Date;
  setCurrentWeek: Function;
};
const WeekDatePicker = ({ date, setCurrentWeek }: WeekPickerProps) => {
  const getWeekRange = (date: Date) => {
    const start = startOfWeek(date, { weekStartsOn: 1 }); // Monday as the first day of the week
    const end = endOfWeek(date, { weekStartsOn: 1 });
    return { start, end };
  };

  const handlePreviousWeek = () => {
    setCurrentWeek(subWeeks(date, 1));
  };

  const handleNextWeek = () => {
    setCurrentWeek(addWeeks(date, 1));
  };

  const { start, end } = getWeekRange(date);

  return (
    <div style={{ textAlign: "center", padding: "10px" }}>
      <button onClick={handlePreviousWeek}>Previous Week</button>
      <span style={{ margin: "0 20px" }}>
        {format(start, "MMM d")} - {format(end, "MMM d")}
      </span>
      <button onClick={handleNextWeek}>Next Week</button>
    </div>
  );
};

export default WeekDatePicker;
