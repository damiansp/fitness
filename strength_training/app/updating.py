import pandas as pd


class Updater:
    def update(self, inpath):
        data = pd.read_csv(inpath)
        data.training_max += data.increment_per_cycle
        data.to_csv(inpath, index=False)

    @staticmethod
    def _update_day(day):
        for ex_type in ['main', 'support']:
            if ex_type  in day:
                day[ex_type] = [
                    (exercise, tr_max + incr, incr)
                    for (exercise, tr_max, incr) in day[ex_type]]
        return day
