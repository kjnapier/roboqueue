import math
from typing import Tuple

DEG_TO_RAD = math.pi / 180.0

def compute_local_sidereal_time(epoch, lon):
    T = (epoch - 2451545.0) / 36525
    theta = 280.46061837 + 360.98564736629 * (epoch - 2451545.0) + (0.000387933 * T * T) - (T * T * T / 38710000.0)
    theta *= DEG_TO_RAD
    return theta + lon

def calc_altaz(ra: float, dec: float, latitude: float, longitude: float, epoch: float) -> Tuple[float, float]:
    """
    Calculate the altitude and azimuth of a celestial object.

    Args:
        ra (float)        : Right ascension of the object, in radians.
        dec (float)       : Declination of the object, in radians.
        latitude (float)  : Equatorial latitude of the observer, in radians.
        longitude (float) : Equatorial longitude of the observer, in radians.
        epoch (float)     : Julian Date in UTC.

    Returns:
        Tuple[float, float]: Altitude and azimuth of the object, in radians.
    """

    # Calculate the local sidereal time.
    local_sidereal_time = compute_local_sidereal_time(epoch, longitude) % (2 * math.pi)

    # Calculate the hour angle.
    hour_angle = local_sidereal_time - ra
    

    # Calculate the altitude.
    altitude = math.asin(math.sin(dec) * math.sin(latitude) + math.cos(dec) * math.cos(latitude) * math.cos(hour_angle))

    # Calculate the azimuth.
    azimuth = math.atan2(math.sin(hour_angle), math.sin(latitude) * math.cos(hour_angle) - math.cos(latitude) * math.tan(dec))

    # Return the altitude and azimuth.
    return altitude, (azimuth + math.pi) % (2 * math.pi)