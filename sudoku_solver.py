#!/usr/bin/env python3
# encoding: utf-8

import os
import sys
import logging

from sudoku import solver
from sudoku import importer
from sudoku import visualizer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main(argv):
    if len(argv) is not 2:
        exit('Aborted. Wrong amount of arguments.')
    file_path = argv[1]
    if not os.path.exists(file_path):
        exit('File does not exists')

    fixed_candidates = importer.imp_candidates(file_path)
    solution = solver.solve(fixed_candidates)
    if solution:
        print('Found solution! {}'.format(solution))
        visualizer.visualize(fixed_candidates+solution)
    else:
        exit('There is no solution')


if __name__ == '__main__':
    main(sys.argv)
