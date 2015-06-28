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


def imp_candidates(path):
    rows = _get_rows(path)
    fix_candidates = []
    for rownumber, row in enumerate(rows, start=1):
        for columnnumber, value in enumerate(row, start=1):
            if not value == '_':
                candidate = 'R{}C{}#{}'.format(rownumber, columnnumber, value)
                fix_candidates.append(candidate)
    return fix_candidates
