import os
import sys
import importer
import logging
import random
from sudoku_matrix import ConstraintMatrix, RowIterator, ColumnIterator
from rules import get_all_satisfied_constraints
from rules import get_all_candidates
import visualizer

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
        visualizer.visualize(solution)
    else:
        log.info('There is no solution')


def get_next_candidate(matrix, constraint, removed_candidates):
    for node in RowIterator(constraint.down):
        if node and node.row_head not in removed_candidates:
            return node.row_head
    return None


def solve(matrix, constraint, result_set,
          covered_candidates = [], covered_constraints = []):
    if not matrix.has_satisfied_all_constraints() and matrix.entry.down:
        log.info('constraint: \t%s', constraint)
        candidate = get_next_candidate(matrix, constraint, covered_candidates)
        for node in ColumnIterator(constraint.down):
            candidate = node.row_head
            if not candidate:
                break
            log.info('candidate: \t%s\n', candidate)
            removed_candidates, removed_constraints = matrix.cover(candidate)
            covered_candidates = covered_candidates + removed_candidates
            covered_constraints = covered_constraints + removed_constraints
            result_set.append(candidate.candidate)
            next_constraint = get_next_constraint(matrix, covered_constraints)
            solve(matrix, next_constraint,
                  result_set, covered_candidates, covered_constraints)
            if matrix.has_satisfied_all_constraints():
                break
            log.info('uncover c: \t%s\n', candidate)
            matrix.uncover(candidate)
            result_set.remove(candidate.candidate)
            covered_candidates = [c for c in covered_candidates if c not in removed_candidates]
            covered_constraints = [c for c in covered_constraints if c not in removed_constraints]

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