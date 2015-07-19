#!/usr/bin/env python3
# encoding: utf-8
import os
import sys

from sudokusolver import solver
from sudokusolver import importer
from sudokusolver import visualizer


def main(argv=sys.argv):
    if len(argv) is not 2:
        exit('Aborted. Wrong amount of arguments.')
    file_path = argv[1]
    if not os.path.exists(file_path):
        exit('File does not exists')

    fixed_candidates = importer.imp_candidates(file_path)
    solution = solver.solve(fixed_candidates)
    if solution:
        visualizer.visualize(fixed_candidates + solution)
    else:
        exit('There is no solution')


if __name__ == '__main__':
    main(sys.argv)
