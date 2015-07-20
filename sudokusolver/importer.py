"""
Provides functions to parse sudoku puzzle from a
text file written in following format::

    _,_,7,  1,_,4,  3,9,_
    9,_,5,  3,2,7,  1,4,8
    3,4,1,  6,8,9,  _,5,2

    5,9,3,  _,6,8,  2,_,1
    _,7,2,  _,1,3,  _,_,9
    6,1,_,  9,7,2,  _,3,5

    _,8,6,  2,3,_,  9,1,4
    1,5,4,  _,9,6,  8,2,3
    _,3,9,  8,4,1,  5,_,_

"""
import csv


# underscore prevents all importing modules to import this method
# when importing with from importer import *
def _get_rows(path):
    with open(path, newline='') as f:
        reader = csv.reader(f)
        rows = []
        for line in reader:
            line = [word.strip() for word in line]
            # ignore empty lines
            if line:
                rows.append(line)
        return rows


def imp_candidates(path: str) -> tuple:
    """Parses a sudoku puzzle and returns the containing numbers
    as strings in the form of ``R{rowNumber}C{columnNumber}#{number}``.
    For example ``R1C1#`` says that in the cell of the first
    row and first column the number one was written into.

    Args:
        path: path to the file containing the sudoku puzzle

    Returns:
        a tuple of strings containing the read numbers 
    """
    rows = _get_rows(path)
    fix_candidates = []
    for rownumber, row in enumerate(rows, start=1):
        for columnnumber, value in enumerate(row, start=1):
            if not value == '_':
                candidate = 'R{}C{}#{}'.format(rownumber, columnnumber, value)
                fix_candidates.append(candidate)
    return tuple(fix_candidates)
