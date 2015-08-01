Usage
=====

Before you can start, you have to install the sudokusolver automatically by pip or manually by hand first.
I recommend pip though:

::

    python3 -m pip install --user git+https://github.com/luxmeter/sudokusolver

You can read how to install pip `here <https://pip.pypa.io/en/stable/installing.html#install-pip/>`_.


Solve sudokus using the CLI
---------------------------

::

    python3 -m sudokusolver sudoku_puzzle.csv

Whereas the csv file follows a particular format pattern:

::

    _,_,4,  9,_,3,  6,_,_
    5,_,6,  2,_,_,  1,3,_
    1,_,_,  8,5,_,  _,9,4

    8,_,_,  1,6,2,  _,4,7
    4,_,_,  _,_,_,  5,6,_
    _,_,_,  7,_,_,  _,_,3

    _,_,_,  6,2,_,  3,_,9
    _,_,_,  _,_,1,  _,_,_
    _,_,2,  _,3,_,  4,_,_


Solve sudokus using the library
-------------------------------

You can use the sudoksusolver also in your application by importing the sudokusolver package.
It contains several modules dealing with the importing, visualization and solving of sudokus.
See the API reference for a detailed description.

To solve a sudoku, you only need the solver module

::

    from sudokusolver import solver
    ...
    solution = solver.solve(fixed_candidates)

The fixed_candidates as well as the solution is a list of strings presenting the numbers written into the cells.
Like the csv file, the strings obey a particular format pattern: ``R{rowNumber}C{columnNumber}#{number}``.

If you want to import a csv file, you can use the importer module:

::

    from sudokusolver import importer
    ...
    fixed_candidates = importer.imp_candidates('sudoku_puzzle.csv')


Build the documentation
-----------------------

::

    python3 setup.py build_sphinx -b html

In order to build the documentation, you have to install `Sphinx <http://sphinx-doc.org/>`_ first.
