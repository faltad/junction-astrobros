from dataclasses import dataclass
from datetime import datetime
import enum


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


class Seasons(enum.StrEnum):
    SPRING = enum.auto()
    WINTER = enum.auto()
    SUMMER = enum.auto()
    AUTUMN = enum.auto()
