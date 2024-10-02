#!/usr/bin/env python3

#------------------------------------------------------------------------------
#
# Usage:
#   ./main [-c CATEGORY] [-t TIME] [-w WORK] [-r REST]
#
#   Where
#   - CATEGORY in [ b | kb | bc | kbc ] (b: boxing, kb: kickboxing, c: circuit)
#   - TIME: total time (min)
#   - WORK: exercise time per round (min)
#   - REST: rest time per round (min)
#
#------------------------------------------------------------------------------

# TODO: make circuit-only option
import argparse
from math import ceil
import os
import sys
from time import sleep, time

from numpy import random


# Moves and weights (frequency in workout is proportional to weight)
BOXING_MOVES = {'jab': 10,
                'cross': 8,
                'left hook': 3,
                'right hook': 3,
                'left uppercut': 3,
                'right uppercut': 3,
                'bob': 0.5,
                'weave': 0.5,
                'circle left': 0.5,
                'circle right': 0.5,
                'block left': 0.25,
                'block right': 0.25}
KICKBOXING_MOVES = {'roundhouse': 3,
                    'side kick': 2,
                    'front kick': 1,
                    'elbow': 1,
                    'knee': 1,
                    'heel kick': 0.3,
                    'inside crescent': 0.25,
                    'outside crescent': 0.1}
EXERCISES = {'pushups': 5,
             'pike pushups': 3,
             'dips': 4,
             'situps': 5,
             'crunches': 5,
             'bicycle situps': 3,
             'plank': 4,
             'leg-lifts': 4,
             'knuckle-dusters': 5,
             'mountain climbers': 3,
             'kettlebell swings': 1,
             'supermans': 2,
             'jumprope': 5,
             'jumping jacks': 5,
             'heismans': 4,
             'speed-skaters': 3,
             'burpees': 2,
             'sprint-sprawl': 3,
             'sprint-sprawl-pushup': 2,
             'squats': 5,
             'lunges': 4,
             'squat jumps': 3,
             'split jumps': 3}
MAX_S_PER_EXERCISE = 30
MAX_COMBO = 5
MOVE_TIME = 1
VOICE = 'Karen'
defaults = {'actual': {'c': 'kbc', 't': 30, 'w': 3., 'r': 1.},
            'test':   {'c': 'kbc', 't': 5, 'w': 2, 'r': 0.1}}

# Dev options
TEST = False
DEFAULTS = defaults['test'] if TEST else defaults['actual']


def main(args):
    args = parse_args(args)
    workout = Workout(**args)
    print(workout)
    workout.start()

    
def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--category',
                        help='workout type (b, kb, bc, kbc)',
                        default=DEFAULTS['c'])
    parser.add_argument('-t', '--time',
                        help='time (min)',
                        type=float,
                        default=DEFAULTS['t'])
    parser.add_argument('-w', '--work',
                        help='work time per round (min)',
                        type=float,
                        default=DEFAULTS['w'])
    parser.add_argument('-r', '--rest',
                        help='rest time per round (min)',
                        type=float,
                        default=DEFAULTS['r'])
    args = parser.parse_args()
    return vars(args)


def say(text):
    os.system(f'say -v {VOICE} {text}')

    
class Workout:
    '''
    Categories:
    - b:   Boxing only        (box, break, box, break...)
    - kb:  Kickboxing only    (kb, break, kb, break...)
    - bc:  Boxing circuit     (b, break, other, break...)
    - kbc: Kickboxing circuit (kb, break, other, break...)
    - c:   Circuit only       (other, break, other, break...)
    '''
    def __init__(self, category, time, work, rest):
        self.cat = category
        self.total_t = time
        self.work_t = work
        round_t = work + rest
        self.n_rounds = int(self.total_t // round_t)
        tot_workout_time = self.n_rounds * self.work_t
        self.rest_t = rest
        self.rounds = self._generate_rounds()

    def __str__(self):
        workout_type = {
            'b': 'boxing',
            'k': 'kickboxing',
            'bc': 'boxing circuit',
            'kbc': 'kickboxing circuit'
        }[self.cat]
        return (f'A {self.total_t} min {workout_type} workout:\n'
                f'{self.n_rounds} rounds of\n'
                f'  Work: {self.work_t:.2f} min\n'
                f'  Rest: {self.rest_t:.2f} min')

    def _generate_rounds(self):
        seq = {
            'b': ['box'],
            'kb': ['kickbox'],
            'bc': ['box', 'other'],
            'kbc': ['kickbox', 'other']
        }[self.cat]
        rounds = []
        while len(rounds) < self.n_rounds:
            rounds += seq
        rounds = rounds[:self.n_rounds]
        return rounds

    def start(self):
        rest_s = int(round(self.rest_t * 60))
        print('Rounds:', self.rounds)
        for rnd in self.rounds:
            r = Round(rnd, self.work_t)
            r.start()
            say(f'Rest for the next {rest_s} seconds')
            sleep(rest_s)


class Round:
    def __init__(self, cat, t):
        self.cat = cat
        self.t = int(round(t * 60))

    def start(self):
        {
            'box': self._start_kboxing,
            'kickbox': self._start_kboxing,
            'other': self._start_other
        }[self.cat](self.cat)

    def _start_kboxing(self, cat):
        moves = BOXING_MOVES
        if cat == 'kickbox':
            moves.update(KICKBOXING_MOVES)
        moves = self._normalize(moves)
        start_time = time()
        elapsed_time = 0
        while elapsed_time < self.t:
            combo = self._get_combo(moves)
            say(combo)
            sleep(MOVE_TIME)
            elapsed_time = time() - start_time

    @staticmethod
    def _get_combo(moves):
        n = random.randint(low=1,high=MAX_COMBO + 1)
        moves = random.choice(
            list(moves.keys()), size=n, replace=True, p=list(moves.values()))
        return ', '.join(moves)

    def _start_other(self, _):
        moves = self._normalize(EXERCISES.copy())
        n_moves = ceil(self.t / MAX_S_PER_EXERCISE)
        time_per_move = self.t / n_moves
        for _ in range(n_moves):
            if not moves:
                moves = self._normalize(EXERCISES.copy())
            move = random.choice(list(moves.keys()), p=list(moves.values()))
            moves.pop(move)
            moves = self._normalize(moves)
            say(move)
            print(move)
            sleep(time_per_move)

    @staticmethod
    def _normalize(dct):
        # Normalize <dct> values to sum to 1
        total = sum(dct.values())
        for k, v in dct.items():
            dct[k] = v / total
        return dct


if __name__ == '__main__':
    main(sys.argv)
