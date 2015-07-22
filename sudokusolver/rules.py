"""
A collection of functions to retrieve the constraints met
by a candidate in a sudoku puzzle and vice-versa.

This module is used by the ``solver`` module to construct
the constraint matrix representing the sudoku puzzle as an exact cover problem.
If you want to solve another exact cover problem by the solver,
you have to pass it a module providing following methods:

    * get_all_candidates
    * get_all_constraints
    * get_all_satisfied_constraints
"""
from collections import defaultdict
from itertools import chain


def _get_row_column_constraints():
    for row in range(1, 10):
        for column in range(1, 10):
            yield 'R{}C{}'.format(row, column)


def _get_row_number_constraints():
    for row in range(1, 10):
        for number in range(1, 10):
            yield 'R{}#{}'.format(row, number)


def _get_column_number_constraints():
    for column in range(1, 10):
        for number in range(1, 10):
            yield 'C{}#{}'.format(column, number)


def _get_block_number_constraints():
    for block in range(1, 10):
        for number in range(1, 10):
            yield 'B{}#{}'.format(block, number)


def _get_satisfied_row_column_constraint(candidate):
    return candidate[0:-2]


def _get_satisfied_row_number_constraint(candidate):
    return ''.join((candidate[0:2], candidate[4:]))


def _get_satisfied_column_number_constraint(candidate):
    return ''.join((candidate[2:4], candidate[4:]))


def _get_satisfied_block_number_constraint(candidate):
    row_index = int(candidate[1:2]) - 1
    column_index = int(candidate[3:4]) - 1
    block_index = (3 * (row_index // 3)) + (column_index // 3)
    block = block_index + 1
    return 'B{}#{}'.format(block, candidate[5:])


def _get_satisfying_values(predicate, constraint=None):
    satisfied_constraints = defaultdict(list)
    for value in get_all_candidates():
        satisfied_constraint = predicate(value)
        if satisfied_constraint:
            satisfied_constraints[satisfied_constraint].append(value)
    if constraint:
        return satisfied_constraints[constraint]
    return satisfied_constraints


def get_all_candidates() -> str:
    """
    Returns all possible numbers for each cell in a sudoku puzzle
    as strings in the format of ``R{rowNumber}C{columnNumber}#{number}``
    - also referred as candidate.

    Returns:
        list of strings of all possible candidates
    """
    result = []
    for row in range(1, 10):
        for column in range(1, 10):
            for number in range(1, 10):
                result.append('R{}C{}#{}'.format(row, column, number))
    return result


def get_all_satisfied_constraints(*candidates: str) -> list:
    """
    Returns all satisfied constraints by a candidate as strings in following format:

    * ``R{number}#{number}`` - describes one of the row constraints, e.g. ``R1#1``.
    * ``C{number}#{number}`` - describes one of the column constraints, e.g. ``C1#1``.
    * ``B{number}#{number}`` - describes one of the block constraints, e.g. ``B1#1``.
    * ``R{number}C{number}`` - describes one of the row-column constraints, e.g. ``R1C1``.

    Args:
        candidates: candidates as strings in form of ``R{rowNumber}C{columnNumber}#{number}``

    Returns:
        list of strings of fulfilled constraints
    """
    res = []
    for p in candidates:
        res += [_get_satisfied_row_column_constraint(p),
                _get_satisfied_row_number_constraint(p),
                _get_satisfied_column_number_constraint(p),
                _get_satisfied_block_number_constraint(p)]
    return res


def get_all_constraints() -> list:
    """
    Returns all constraints of a sudoku puzzle as strings in the following format:

    * ``R{number}#{number}`` - describes one of the row constraints, e.g. ``R1#1``.
    * ``C{number}#{number}`` - describes one of the column constraints, e.g. ``C1#1``.
    * ``B{number}#{number}`` - describes one of the block constraints, e.g. ``B1#1``.
    * ``R{number}C{number}`` - describes one of the row-column constraints, e.g. ``R1C1``.

    Returns
        list of strings of all constraints
    """
    return chain(_get_row_column_constraints(), _get_row_number_constraints(),
                 _get_column_number_constraints(),
                 _get_block_number_constraints())
