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
        print('Found solution!')
        visualizer.visualize(fixed_candidates + solution)
    else:
        exit('There is no solution')


def solve(fixed_candidates):
    matrix = _create_matrix(fixed_candidates)
    solution = []
    _solve(matrix, solution)
    return solution if matrix.has_satisfied_all_constraints() else []


def _solve(matrix, result_set,
           covered_candidates=[], covered_constraints=[]):
    if not matrix.has_satisfied_all_constraints() and matrix.entry.down:
        constraint = _get_next_constraint(matrix, covered_constraints)
        for node in ColumnIterator(constraint.down):
            candidate = node.row_head
            if not candidate:
                break
            removed_candidates, removed_constraints = matrix.cover(candidate)
            covered_candidates = covered_candidates + removed_candidates
            covered_constraints = covered_constraints + removed_constraints
            result_set.append(candidate.candidate)
            _solve(matrix, result_set, covered_candidates, covered_constraints)
            if matrix.has_satisfied_all_constraints():
                break
            matrix.uncover(candidate)
            result_set.remove(candidate.candidate)
            covered_candidates = [c for c in covered_candidates if
                                  c not in removed_candidates]
            covered_constraints = [c for c in covered_constraints if
                                   c not in removed_constraints]


def _get_next_constraint(matrix, covered_constraints):
    for c in RowIterator(matrix.entry.right):
        if c not in covered_constraints:
            return c
    return None


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
