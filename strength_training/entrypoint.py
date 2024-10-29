#! /usr/bin/env python3

#----------------------------------------------------------------------
#
# Usage
# entrypoint.py [-i INFILE][-o OUTFILE][-w UPDATE]
#
# -i: input file name:
#     INFILE (str): name of input file (defaults to "input.csv")
# -o: output file name:
#     OUTFILE (str): name of output file (defaults to "schedule.csv")
# -w: Updates available weights:
#     UPDATE (str): true | false (defaults to false)
#
#----------------------------------------------------------------------
import argparse
import sys

from app.input_handling import InputReader
from app.scheduler import Scheduler
from app.updating import Updater
from app.weight_chart import WeightChart

DATA = './data'


def main(args):
    infile, outfile, do_weight_update = parse_args(args)
    print(
        f'Running with args:\n'
        f'  infile:         {infile}\n'
        f'  outfile:        {outfile}\n'
        f'  update_weights: {do_weight_update}')
    if do_weight_update:
        update_weights()
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
    parser.add_argument(
        '-w',
        '--weight_update',
        help='if -w, available weights will be updated',
        default='false')
    args = parser.parse_args()
    return (
        [check_extensions(f) for f in (args.infile, args.outfile)]
        + [args.weight_update.lower() == 'true'])


def check_extensions(filename):
    if not filename.endswith('.csv'):
        filename += '.csv'
    return filename


def update_weights():
    print('Updating weights...')
    for bell in ['bar', 'dumb']:
        WeightChart().make_chart(bell)

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
