

class TargetList:

    def __init__(self):
        self.targets = []

    def add_target(self, target):
        self.targets.append(target)

    def at(self, epoch, telescope, conditions):
        ras = []
        decs = []
        alts = []
        azs = []
        exptimes = []

        for target in self.targets:
            ra, dec, alt, az, exptime = target.at(epoch, telescope, conditions)
            ras.append(ra)
            decs.append(dec)
            alts.append(alt)
            azs.append(az)
            exptimes.append(exptime)

        return ras, decs, alts, azs, exptimes
    
