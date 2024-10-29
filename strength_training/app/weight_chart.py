import numpy as np
import pandas as pd


DATA = './data/weights'


class WeightChart:
    def make_chart(self, dumb_bar: str):
        '''Makes a chart of all possible weight combinations given your weights
        Args:
        - dumb_bar: either "dumb" or "bar"
        '''
        bar, half_plates = self._read_weights(dumb_bar)
        df = self._init_data(half_plates)
        out = self._compile_df(df, bar)
        outpath = f'{DATA}/{dumb_bar}_combos.csv'
        out.to_csv(outpath, index=False)        

    @staticmethod
    def _read_weights(dumb_bar):
        path = f'{DATA}/{dumb_bar}_weights.csv'
        data = pd.read_csv(path, index_col=0)
        bar = data.index[0]
        plates = []
        for weight in data.columns:
            n = data.loc[bar, weight]
            if n % 2:
                n -= 1
                print(
                    'Warning: Odd number of plates found. Ignoring unbalanced '
                    'plates')
            plates += [float(weight)] * (n // 2)
        return bar, plates

    @staticmethod
    def _init_data(half_plates):
        n_plates = len(half_plates)
        n_combos = 2 ** n_plates
        data = [
            [int(i) for i in list(f'{str(bin(n))[2:]:>0{n_plates}s}')]
            for n in range(n_combos)]
        df = pd.DataFrame(
            np.array(data) * np.array(half_plates), columns=half_plates)
        return df

    @staticmethod
    def _compile_df(df, bar):
        df['weight'] = bar + 2*df.sum(axis=1)
        return (
            df
            .drop_duplicates(subset=['weight'])
            .sort_values('weight', ignore_index=True))


if __name__ == '__main__':
    WeightChart().make_chart('bar')
    WeightChart().make_chart('dumb')
