"""Provides mechanism to visualize sudoku puzzles"""
import re

from collections import defaultdict


def visualize(candidates):
    """Print the sudoku puzzle on the std. output.
    The candidates are a list of strings each representing
    a number in a cell. Therefore they obey a particular format
    pattern, R{rowNumber}C{columnNumber}#{number}.
    For example R1C1#1 means that the cell in the first row
    and first column containts the number one.

    Args:
        candidates - sequence of strings representing a number in a cell
    """
    matrix = _map_by_label(candidates)
    for row in matrix.keys():
        if row != 0 and row % 3 == 0:
            print('')
        numbers = [str(n) for n in matrix[row].values()]
        for i, number in enumerate(numbers):
            if i != 0 and i % 3 == 0:
                numbers[i] = ' |' + number
        print('|' + '|'.join(numbers) + '|')


def _map_by_label(candidates):
    matrix = defaultdict(dict)
    for candidate in candidates:
        pattern = re.compile(r'R(\d)C(\d)#(\d)')
        matches = pattern.match(candidate)
        row = int(matches.group(1))
        column = int(matches.group(2))
        number = int(matches.group(3))
        matrix[(row - 1)][(column - 1)] = number
    return matrix
