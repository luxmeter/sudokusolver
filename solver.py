import os
import sys
import logging

import importer
from sudoku_matrix import ConstraintMatrix, RowIterator, ColumnIterator
from rules import get_all_satisfied_constraints
from rules import get_all_candidates
import visualizer

logging.basicConfig(level=logging.INFO)


def main(argv):
    if len(argv) is not 2:
        exit('Aborted. Wrong amount of arguments.')
    file_path = argv[1]
    if not os.path.exists(file_path):
        exit('File does not exists')

    fixed_candidates = importer.imp_candidates(file_path)
    solution = solve(fixed_candidates)
    if solution:
        print('Found solution! {}'.format(solution))
        visualizer.visualize(fixed_candidates+solution)
    else:
        exit('There is no solution')

def solve(fixed_candidates):
    matrix = _create_matrix(fixed_candidates)
    solution = _solve(matrix)
    return solution if matrix.has_satisfied_all_constraints() else []

def _solve(matrix, result_set=()):
    # there are still candidates left
    if matrix.exists_candidates():
        for candidate in matrix.get_next_candidate():
            matrix.cover(candidate)
            solution = _solve(matrix, result_set + (candidate.candidate, ))
            if matrix.has_satisfied_all_constraints():
                return solution
            matrix.uncover()
    return result_set

def _create_matrix(fixed_candidates):
    matrix = ConstraintMatrix()
    fixed_constraints = get_all_satisfied_constraints(*fixed_candidates)
    for candidate in get_all_candidates():
        satisfied_constraints = get_all_satisfied_constraints(candidate)
        if candidate not in fixed_candidates \
                and not (set(fixed_constraints) & set(satisfied_constraints)):
            matrix.add(candidate, satisfied_constraints)
    return matrix


if __name__ == '__main__':
    main(sys.argv)
