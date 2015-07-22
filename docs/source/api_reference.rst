API Reference
=============

.. automodule:: sudokusolver
   :members:


Candidates and Constraints
--------------------------

A candidate in terms of sudokus is simply a number in one of the cells in the grid.
Those candidates are related to one or more of the constraints of the sudoku.
In total, there exists :math:`9^3 = 729` candidates since
each of the 81 cells can contain 9 numbers and :math:`9^2 * 4 = 324` constraints
that cover all four kind of constraints (Row-Number, Column-Number, Block-Numer and Row-Column).

The API doesn't force you to use some dedicated data structures
to describe the sudoku puzzle. Instead you can use simple strings that identify
the candidate and constraints. When you want to use the core API to apply it to another
exact cover problem, you can define your own format pattern.
However, if you want to use it to solve a sudoku, you have to obey following pattern:

For candidates:

::

    # e.g. first column, first row, number 1
    # R1C1#1
    R{rowNumber}C{columnNumber}#{number}

For constraints:

::

    R{rowNumber}#{number}               # e.g. R#1
    C{columnNumber}#{number}            # e.g. C#1
    B{blockNumber}#{number}             # e.g. B#1
    R{rowNumber}C{columnNumber}         # e.g. R1C1


The “importer” module
---------------------

.. automodule:: sudokusolver.importer
    :members:


The “visualizer” module
-----------------------

.. automodule:: sudokusolver.visualizer
    :members:


The “solver” module
-------------------

.. automodule:: sudokusolver.solver
    :members:


The “model” module
-------------------

.. automodule:: sudokusolver.model
    :members:

The “model.node” module
~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: sudokusolver.model.node
   :members: Node, RowReferenceNode, ColumnReferenceNode, MatrixHeadReferenceNode

The “model.iterators” module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: sudokusolver.model.iterators
   :members:

The “model.constraintmatrix” module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: sudokusolver.model.constraintmatrix
   :members:
