"""
Module used to solve sudoku puzzles.
"""
from .model.constraintmatrix import ConstraintMatrix
from .rules import get_all_satisfied_constraints, get_all_candidates


def solve(fixed_candidates):
    """
    Solves a sudoku puzzle by applying the exact cover problem on it.
    The puzzle is described here as sequence of 'fixed candidates'
    which are nothing more than strings representing the already filled in numbers.
    Those strings obey are particular format pattern to identify the cells
    in which the numbers were filled in: R{rowNumber}C{columnNumber}#{number}.
    For example R1C1#1 means that in the cell of the first row and first column
    the number one was written into.

    The return value is also list of candidates which solve the sudoku.

    Args:
        fixed_candidates: cells with their numbers

    Returns:
        list of candidates solving the sudoku puzzle
    """
    matrix = _create_matrix(fixed_candidates)
    solution = _solve(matrix)
    return solution if matrix.has_satisfied_all_constraints() else []


def _solve(matrix, result_set=()):
    if matrix.candidates_exist():
        for candidate in matrix.get_next_constraints_candidates():
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
