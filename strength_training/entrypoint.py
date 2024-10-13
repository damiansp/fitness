#! /usr/bin/env python3

#----------------------------------------------------------------
#
# Usage
# entrypoint.py [-i INFILE][-o OUTFILE]
#
# INFILE (str): name of input file (defaults to "input.csv")
# OUTFILE (str): name of output file (defaults to "schedule.csv")
#
#----------------------------------------------------------------
import argparse
import sys

from app.input_handling import InputReader
from app.scheduler import Scheduler
from app.updating import Updater


DATA = './data'


def main(args):
    infile, outfile = parse_args(args)
    print(
        f'Running with args:\n'
        f'  infile:  {infile}\n'
        f'  outfile: {outfile}')
    create_cycle_from_input_file(infile, outfile)


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--infile',
        help='Input file name (e.g., "input.csv")',
        default='input.csv')
    parser.add_argument(
        '-o',
        '--outfile',
        help='Output file name (e.g., "schedule.csv")',
        default='schedule.csv')
    args = parser.parse_args()
    return [check_extensions(f) for f in (args.infile, args.outfile)]


def check_extensions(filename):
    if not filename.endswith('.csv'):
        filename += '.csv'
    return filename


def create_cycle_from_input_file(infile, outfile):
    print(f'Creating cycle from {infile}...')
    exercises = InputReader().get_exercises(f'{DATA}/{infile}')
    schedule = Scheduler(exercises, is_extended=True).make_schedule()
    sched_path = f'{DATA}/{outfile}'
    schedule.to_csv(sched_path, index=False)
    print('Saved schedule to', sched_path)
    Updater().update(f'{DATA}/{infile}')
    print(f'Input file {infile} updated for next cycle')
    

if __name__ == '__main__':
    main(sys.argv)
