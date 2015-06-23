import os
import sys
import importer
import logging
from sudoku_matrix import ConstraintMatrix, RowIterator, ColumnIterator
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

    matrix = _create_matrix(importer.imp_candidates(file_path))
    solve(matrix, RowIterator(matrix.get_unsatisfied_constraint_column()))

def solve(matrix, constraint_iterator, result_set=()):
    constraint = next(constraint_iterator, None)
    log.info('resolving constraint \t%s', constraint)
    for column_node in ColumnIterator(constraint):
        if column_node.candidate is not '_':
            candidate = column_node.row_head
            new_result_set = result_set + (candidate,)
            log.info('checking candidate \t%s', candidate.candidate)
            matrix.cover(candidate)
            if matrix.has_satisfied_all_constraints():
                return new_result_set
            else:
                solve(matrix, ColumnIterator(constraint.right), new_result_set)
            if matrix.has_satisfied_all_constraints():
                return new_result_set
            # log.info('candidate discarded \t%s', candidate.candidate)
            matrix.uncover(candidate)
    if matrix.has_satisfied_all_constraints():
        return new_result_set
    log.info('no solution found')
    return None

def _create_matrix(fixed_candidates):
    matrix = ConstraintMatrix()
    for candidate in get_all_candidates():
        if candidate not in fixed_candidates:
            satisfied_constraints = get_all_satisfied_constraints(candidate)
            matrix.add(candidate, satisfied_constraints)
    return matrix


if __name__ == '__main__':
    main(sys.argv)