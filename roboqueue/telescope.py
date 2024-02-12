from spacerocks.observer import Observer
import numpy as np

class Telescope:

    def __init__(self, obscode: str, filter: str):

        self.obscode = obscode
        self.filter = filter

        o = Observer.from_obscode(obscode)
        self.lat = np.radians(o.lat[0])
        self.lon = np.radians(o.lon[0])
