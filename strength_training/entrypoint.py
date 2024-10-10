import json
import pickle

import pandas as pd

from app.scheduler import Schedule


DATA = './data'


def main():
    exercises = InputReader(f'{DATA}/input.csv').get_exercises()
    schedule = Schedule(exercises, is_extended=True).make_schedule()
    sched_path = f'{DATA}/test_schedule.csv'
    schedule.to_csv(sched_path, index=False)
    print('Saved schedule to', sched_path)
    

class InputReader:
    def __init__(self, path):
        self.path = path
        
    def get_exercises(self):
        ext = self.path.split('.')[-1]
        exercises = {
            'csv': self._get_exercises_from_csv,
            'json': self._get_exercises_from_json,
            'pkl': self._get_exercises_from_pickle
        }[ext]()
        return exercises
    
    def _get_exercises_from_csv(self):
        df = pd.read_csv(self.path)
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
            

    def _get_exercises_from_json(self):
        with open(self.path, 'r') as f:
            exercises = json.load(f)
        # Convert innermost lists to tuples
        for day in exercises:
            for k, v in day.items():
                exercises[day][k] = [tuple(x) for x in v]
        return exercises

    def _get_exercises_from_pickle(self):
        with open(self.path, 'rb') as f:
            exercises = pickle.load(f)
        return exercises


if __name__ == '__main__':
    main()
