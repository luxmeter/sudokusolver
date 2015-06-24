import os
import sys
import importer
import logging
import random
from sudoku_matrix import ConstraintMatrix, RowIterator
from rules import get_all_satisfied_constraints
from rules import get_all_candidates

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def main(argv):
    if len(argv) is not 2:
        exit('Aborted. Wrong amount of arguments.')
    file_path = argv[1]
    if not os.path.exists(file_path):
        exit('File does not exists')

    matrix = create_matrix(importer.imp_candidates(file_path))
    solution = []
    solve(matrix, get_next_constraint(matrix, []), solution)
    if matrix.has_satisfied_all_constraints():
        log.info('Found solution: %s', solution)
    else:
        log.info('There is no solution')


def solve(matrix, constraint, result_set, covered_constraints = []):
    if not matrix.has_satisfied_all_constraints() and matrix.entry.down:
        log.info('constraint: \t%s', constraint)
        candidates = [candidate.row_head for candidate in
                      create_column_generator(constraint)]
        for candidate in candidates:
            covered_constraints = covered_constraints + matrix.cover(candidate)
            result_set.append(candidate.candidate)
            solve(matrix, get_next_constraint(matrix, covered_constraints), result_set, covered_constraints)
            if matrix.has_satisfied_all_constraints():
                break
            covered_constraints = [c for c in matrix.uncover(candidate)]
            result_set.remove(candidate.candidate)


def get_next_constraint(matrix, covered_constraints):
    for c in RowIterator(matrix.entry.right):
        if c not in covered_constraints:
            return c
    return None


def create_column_generator(column_head):
    node = column_head
    while node:
        node = node.down
        if node:
            yield node

def create_row_generator(row_head):
    node = row_head
    while node:
        node = node.right
        if node:
            yield node

def create_matrix(fixed_candidates):
    matrix = ConstraintMatrix()
    fixed_constraints = get_all_satisfied_constraints(*fixed_candidates)
    for candidate in get_all_candidates():
        satisfied_constraints = get_all_satisfied_constraints(candidate)
        if candidate not in fixed_candidates\
                and not(set(fixed_constraints) & set(satisfied_constraints)):
            matrix.add(candidate, satisfied_constraints)
    return matrix


if __name__ == '__main__':
    main(sys.argv)