from dataclasses import dataclass
from datetime import datetime


@dataclass
class Coords:
    south_east_latitude: float
    south_east_longitude: float
    north_west_latitude: float
    north_west_longitude: float


@dataclass
class DateRange:
    start_date: datetime
    end_date: datetime
