import logging

from .constraintmatrix import ConstraintMatrix
from .rules import get_all_satisfied_constraints
from .rules import get_all_candidates

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def solve(fixed_candidates):
    matrix = _create_matrix(fixed_candidates)
    solution = _solve(matrix)
    return solution if matrix.has_satisfied_all_constraints() else []


def _solve(matrix, result_set=()):
    # there are still candidates left
    if matrix.exists_candidates():
        for candidate in matrix.get_next_constraints_candidates():
            # log.info('try candidate: %s' % candidate)
            matrix.cover(candidate)
            solution = _solve(matrix, result_set + (candidate.candidate, ))
            if matrix.has_satisfied_all_constraints():
                return solution
            # log.info('uncover candidate: %s' % candidate)
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