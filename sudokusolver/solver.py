"""
Module used to solve sudoku puzzles.
"""
from sudokusolver import rules
from .model.constraintmatrix import ConstraintMatrix


def solve(fixed_candidates, rule_description=None) -> list:
    """
    Solves by default a sudoku puzzle by applying the exact cover problem to it
    and using the Algorithm-X by Donald Knuth.
    The puzzle is described here as sequence of strings describing the *fixed candidates*::
    
        R{rowNumber}C{columnNumber}#{number}

    The return value is also list of candidates which solve the sudoku.
    
    Note:

        The second argument can be used to solve other exact cover problems than sudoku.
        See documentation for further information.

    Args:
        fixed_candidates: list of strings describing the filled in cells with their numbers
        rule_description: lookup for candidates and constraints of sudoku

    Returns:
        list of strings describing the candidates solving the sudoku puzzle
    """
    rule_description = rules if not rule_description else rule_description
    matrix = _create_matrix(fixed_candidates, rule_description)
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


def _create_matrix(fixed_candidates, rule_description):
    matrix = ConstraintMatrix()
    fixed_constraints = rule_description.get_all_satisfied_constraints(*fixed_candidates)
    for candidate in rule_description.get_all_candidates():
        satisfied_constraints = rule_description.get_all_satisfied_constraints(candidate)
        if candidate not in fixed_candidates \
                and not (set(fixed_constraints) & set(satisfied_constraints)):
            matrix.add(candidate, satisfied_constraints)
    return matrix
