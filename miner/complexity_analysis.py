#!/usr/bin/env python
######################################################################
## This program calculates the whitespace complexity of a file.
######################################################################

import argparse
import os
import desc_stats
import complexity_calculations
import csv_writer
import json_writer


######################################################################
# Statistics from complexity
######################################################################


def as_stats(revision, complexity_by_line):
    return desc_stats.DescriptiveStats(revision, complexity_by_line)


######################################################################
## Output
######################################################################

def print_heading():
    print('file_path,n,total,mean,sd,max')


def as_csv(filename, stats):
    fields_of_interest = [stats.n_revs, stats.total, round(stats.mean(), 2), round(stats.sd(), 2), stats.max_value()]
    printable = [str(field) for field in fields_of_interest]
    print(filename + ',' + ','.join(printable))


######################################################################
# Main
######################################################################


def run_file(filename, writer):
    with open(filename, "r") as file_to_calc:
        complexity_by_line = complexity_calculations.calculate_complexity_in(file_to_calc.read())
        stats = desc_stats.DescriptiveStats(filename, complexity_by_line)
        writer.print_stats(filename, stats)


dirs_to_ignore = ['.git', '.idea']
file_endings_to_ignore = {'jpg', 'jpeg', 'png', 'gif', 'psd', 'ttf', 'xap', 'woff', 'db', 'otf', 'bmp', 'ico', 'png',
                          'svg', 'swf', 'eot', 'pdf'}


def run_iterative(path, writer):
    for root, subdirs, files in os.walk(path):
        for directory in dirs_to_ignore:
            if directory in subdirs:
                subdirs.remove(directory)

        for filename in files:
            ending = filename.split('.')[-1]
            if ending.lower() not in file_endings_to_ignore:
                file_path = os.path.join(root, filename)
                run_file(file_path, writer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculates whitespace complexity of the given file.')
    parser.add_argument('path', type=str, help='The path to calculate complexity from')
    parser.add_argument('--recursive', dest='recursive', action='store_true',
                        help='recursively apply to all files in path')
    parser.add_argument('--json',
                        dest='writer',
                        action='store_const',
                        const=json_writer.JsonWriter,
                        default=csv_writer.CsvWriter,
                        help='recursively apply to all files in path')
    args = parser.parse_args()
    writer = args.writer()
    writer.print_header()
    if args.recursive:
        run_iterative(args.path, writer)
    else:
        run_file(args.path, writer)
    writer.print_footer()
