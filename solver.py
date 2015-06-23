import os
import sys
import importer
import logging
import random
from sudoku_matrix import ConstraintMatrix
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
    solution = solve(matrix, create_row_generator(
        matrix.get_unsatisfied_constraint_column()))
    if matrix.has_satisfied_all_constraints():
        log.info('Found solution: %s', solution)
    else:
        log.info('There is no solution')

def solve(matrix, constraint_generator, result_set=()):
    if matrix.has_satisfied_all_constraints():
        return result_set
    constraint = next(constraint_generator, None)
    if constraint and constraint.down:
        log.info('resolving constraint \t%s', constraint.covered_constraint)
        candidates = [candidate.row_head for candidate in
                      create_column_generator(constraint)]
        # random.shuffle(candidates, random.random)
        for candidate in candidates:
            log.info('checking candidate \t%s', candidate.candidate)
            new_result_set = result_set + (candidate,)
            matrix.cover(candidate)
            new_result_set = solve(matrix, create_row_generator(constraint.right), new_result_set)
            if matrix.has_satisfied_all_constraints():
                return new_result_set
            matrix.uncover(candidate)
    log.info('solution not found')
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