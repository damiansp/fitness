import pandas as pd


class InputReader:
    def get_exercises(self, path):
        df = pd.read_csv(path)
        exercises = []
        for day in df['day'].unique():
            day_exercises = self._get_exercises_for_day(
                df.loc[df.day == day, :])
            exercises.append(day_exercises)
        return exercises

    @staticmethod
    def _get_exercises_for_day(day_df):
        main = []
        support = []
        for _, row in day_df.iterrows():
            tup = (row.exercise, row.training_max, row.increment_per_cycle)
            if row['type'] == 'main':
                main.append(tup)
            elif row['type'] == 'support':
                support.append(tup)
            else:
                raise ValueError(f'Bad "type": {row["type"]}')
        return {'main': main, 'support': support}
