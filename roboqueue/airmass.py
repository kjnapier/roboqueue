import math
import numpy as np

def calculate_airmass(altitude: float) -> float:
    """
    Calculate the airmass of an object.

    Args:
        altitude (float): Altitude of the object, in radians.

    Returns:
        float: Airmass of the object.
    """

    # Calculate the airmass.
    if altitude < 0:
        return np.inf
    return 1 / math.sin(np.radians(np.degrees(altitude) + 244 / (165 + 47 * np.degrees(altitude) ** 1.1)))