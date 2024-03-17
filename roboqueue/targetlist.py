

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
        dones = []

        for target in self.targets:
            ra, dec, alt, az, exptime, is_done = target.at(epoch, telescope, conditions)
            ras.append(ra)
            decs.append(dec)
            alts.append(alt)
            azs.append(az)
            exptimes.append(exptime)
            dones.append(is_done)

        return ras, decs, alts, azs, exptimes, dones
    
    def __len__(self):
        return len(self.targets)
    
    def __getitem__(self, idx):
        return self.targets[idx]
    
    def remove(self, target):
        self.targets.remove(target)
    
