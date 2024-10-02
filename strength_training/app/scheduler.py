import pandas as pd


class Exercise:
    def __init__(self, name:str, training_max: float, reps_percents):
        self.name = name
        self.training_max = training_max
        self.reps_percents = reps_percents

    def make_row(self):
        row = pd.concat([self._make_week(w) for w in range(1, 5)], axis=1)
        row.index = [self.name] * len(row)
        return row                        

    def _make_week(self, week):
        reps_percents = self.reps_percents[f'week{week}']
        data = [[r, p * self.training_max] for (r, p) in reps_percents]
        df = pd.DataFrame(
            data,
            columns=pd.MultiIndex.from_tuples(
                [(f'Week {week}', 'Reps'), (f'Week {week}', 'Weight')]))
        return df        


class MainExercise(Exercise):
    def __init__(
            self, name: str, training_max: float, is_extended: bool = False):
        reps_percents = {
            # (reps, % of max)
            'week1': [
                (5, 0.4), (5, 0.47), (3, 0.55), (5, 0.65), (5, 0.75), (5, 0.85)
            ],
            'week2': [
                (5, 0.4), (5, 0.5), (3, 0.6), (3, 0.7), (3, 0.8), (3, 0.9)],
            'week3': [
                (5, 0.4), (5, 0.5), (3, 0.6), (5, 0.75), (3, 0.85), (1, 0.95)],
            # Deload week
            'week4': [
                (0, 0), (0, 0), (0, 0), (5, 0.4), (5, 0.5), (5, 0.6)]}
        if not is_extended:
            reps_percents = {k: v[3:] for k, v in reps_percents.items()}
        super().__init__(name, training_max, reps_percents)


class SupportingExercise(Exercise):
    def __init__(self, name: str, training_max: float):
        reps_percents = {
            # (reps, % of max)
            'week1': [('5x10', 0.85)],
            'week2': [('5x10', 0.9)],
            'week3': [('5x10', 0.95)],
            # Deload week
            'week4': [('5x10', 0.6)]}
        super().__init__(name, training_max, reps_percents)


class ScheduleRow:
    def __init__(
            self,
            main_exercise: MainExercise,
            supporting_exercises: tuple[SupportingExercise]):
        self.main_exercise = main_exercise
        self.supporting_exercises = supporting_exercises

    def make_row(self):
        df = pd.concat(
            [self.main_exercise.make_row(),
             *[se.make_row() for se in self.supporting_exercises]])
        return df


class Schedule:
    def __init__(self, exercises: list[dict], is_extended: bool = False):
        '''Make a work out schedule for one (4-week) cycle
        Args:
        - exercises: each entry is a single day's exercises, formatted as:
          [
              # 1st Day
              {
                   'main': (name, training_max)},
                   'support': [
                       (name1, tr_mx1), (name2, tr_mx2), ..., (namen, tr_mxn)
                    ]
              },
              # 2nd Day
              {
                   'main': [name, training_max]},
                   'support': [
                       (name1, tr_mx1), (name2, tr_mx2), ..., (namen, tr_mxn)
                    ]
              },
              {...}
          ]
        - is_extended: if True does long form (more sets for main exercise)
        '''
        self.exercises = exercises
        self.is_extended = is_extended

    def make_schedule(self):
        dfs = []
        for i, day in enumerate(self.exercises):
            main_exercise = MainExercise(
                *day['main'], is_extended=self.is_extended)
            supporting_exercises = [
                SupportingExercise(name, tr_mx)
                for (name, tr_mx) in day['support']]
            row = ScheduleRow(main_exercise, supporting_exercises).make_row()
            row.index = pd.MultiIndex.from_tuples(
                [(i + 1, idx) for idx in row.index])
            dfs.append(row)
        df = pd.concat(dfs)
        return df



if __name__ == '__main__':
    #print(MainExercise('Squat', 188).make_row())
    #print(SupportingExercise('GM Standing', 76.5).make_row())

    #main_ex = MainExercise('Squat', 188)
    #support = [
    #    SupportingExercise('GM Standing', 76.5),
    #    SupportingExercise('DB Lunge', 69.5),
    #    SupportingExercise('Situps', 17.1)]
    #print(ScheduleRow(main_ex, support).make_row())

    exercises = [
        {'main': ('Squat', 188.),
         'support': [
             ('GM Standing', 76.5), ('DB Lunge', 69.5), ('Situp', 17.1)]},
        {'main': ('Bench', 139.),
         'support': [
             ('DB Flies', 69.5), ('Wide Dips', 14.54), ('Knuckle Duster', 24.)
         ]},
        {'main': ('Deadlift', 215.),
         'support': [
             ('DB Skull Crusher', 20.75),
             ('Kroc Rows', 39.5),
             ('Situps', 17.1)]},
        {'main': ('Overhead Press', 106.5),
         'support': [('Pullup', 10.), ('Curl', 20.75), ('Knuckle Duster', 24.)]
        }]
    print(Schedule(exercises, is_extended=True).make_schedule())
    
