######################################################################
## This program calculates the whitespace complexity of a file.
######################################################################

#!/bin/env python
import argparse
import os
import desc_stats
import complexity_calculations

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
	fields_of_interest = [stats.n_revs, stats.total, round(stats.mean(),2), round(stats.sd(),2), stats.max_value()]
	printable = [str(field) for field in fields_of_interest]
	print(filename + ',' + ','.join(printable))

######################################################################
# Main
######################################################################


def run_file(filename):
	with open(filename, "r") as file_to_calc:
		complexity_by_line = complexity_calculations.calculate_complexity_in(file_to_calc.read())
		stats = desc_stats.DescriptiveStats(filename, complexity_by_line)
		as_csv(filename, stats)


dirs_to_ignore = ['.git', '.idea']
file_endings_to_ignore = {'jpg', 'jpeg', 'png', 'gif', 'psd', 'ttf', 'xap', 'woff', 'db', 'otf', 'bmp', 'ico', 'png', 'svg', 'swf', 'eot', 'pdf'}


def run_iterative(path):

	for root, subdirs, files in os.walk(path):
		if '.git' in subdirs:
			subdirs.remove('.git')
		if '.idea' in subdirs:
			subdirs.remove('.idea')

		for filename in files:
			ending = filename.split('.')[-1]
			if ending.lower() not in file_endings_to_ignore:
				file_path = os.path.join(root, filename)
				run_file(file_path)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Calculates whitespace complexity of the given file.')
	parser.add_argument('path', type=str, help='The path to calculate complexity from')
	parser.add_argument('--recursive', dest='recursive', action='store_true', help='recursively apply to all files in path')
	args = parser.parse_args()
	print_heading()
	if args.recursive:
		run_iterative(args.path)
	else:
		run_file(args.path)

