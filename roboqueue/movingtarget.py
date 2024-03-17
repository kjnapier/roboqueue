from spacerocks.spacerock import SpaceRock
import numpy as np

from .expcal import calculate_exposure_time
from .altaz import calc_altaz
from .airmass import calculate_airmass

DEG_TO_RAD = np.pi / 180
RAD_PER_ARCSEC = 180 / np.pi * 3600
HOUR_PER_DAY = 24

class MovingTarget:

    def __init__(self, rock: SpaceRock, required_snr: float):
        self.name = rock.name
        self.rock = rock
        self.required_snr = required_snr
        self.done = False

    def at(self, epoch, telescope, conditions):
        self.rock.analytic_propagate(epoch)
        o = self.rock.observe(obscode=telescope.obscode)

        ra = o.ra.rad[0]
        dec = o.dec.rad[0]
        ra_rate = o.ra_rate[0]
        dec_rate = o.dec_rate[0]
        proper_motion = np.sqrt(ra_rate**2 * np.cos(dec)**2 + dec_rate**2).value * RAD_PER_ARCSEC / HOUR_PER_DAY

        alt, az = calc_altaz(ra, dec, telescope.lat, telescope.lon, epoch)
        airmass = calculate_airmass(alt)
        mag = o.mag[0]
        required_exposure_time = calculate_exposure_time(self.required_snr, 
                                                         mag=mag, 
                                                         airmass=airmass, 
                                                         ext_coeff=-0.31, 
                                                         seeing=conditions.seeing, 
                                                         rate=proper_motion, 
                                                         Filter=telescope.filter, 
                                                         moon=conditions.moon, 
                                                         niter=10)

        return ra, dec, alt, az, required_exposure_time, self.done
