from spacerocks.observing import Observatory
import numpy as np

class Telescope:

    def __init__(self, obscode: str, filter: str):

        self.obscode = obscode
        self.filter = filter

        o = Observatory.from_obscode(obscode)
        self.lat = o.lat
        self.lon = o.lon
