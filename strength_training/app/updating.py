import pandas as pd


class Updater:
    def update(self, inpath):
        data = pd.read_csv(inpath)
        data.training_max += data.increment_per_cycle
        data.to_csv(inpath, index=False)
