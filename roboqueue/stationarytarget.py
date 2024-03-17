from spacerocks.spacerock import SpaceRock
import numpy as np

from .expcal import calculate_exposure_time
from .altaz import calc_altaz
from .airmass import calculate_airmass

DEG_TO_RAD = np.pi / 180
RAD_PER_ARCSEC = 180 / np.pi * 3600
HOUR_PER_DAY = 24

class StationaryTarget:

    def __init__(self, name: str, ra: float, dec: float, mag: float, required_snr: float):
        self.name = name
        self.ra = ra
        self.dec = dec
        self.mag = mag
        self.required_snr = required_snr
        self.done = False

    def at(self, epoch, telescope, conditions):
        
        alt, az = calc_altaz(self.ra, self.dec, telescope.lat, telescope.lon, epoch)
        airmass = calculate_airmass(alt)
        required_exposure_time = calculate_exposure_time(self.required_snr, 
                                                         mag=self.mag, 
                                                         airmass=airmass, 
                                                         ext_coeff=-0.31, 
                                                         seeing=conditions.seeing, 
                                                         rate=0.0, 
                                                         Filter=telescope.filter, 
                                                         moon=conditions.moon, 
                                                         niter=10)

        return self.ra, self.dec, alt, az, required_exposure_time, self.done