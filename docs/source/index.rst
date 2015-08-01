.. sudokusolver documentation master file, created by
   sphinx-quickstart on Mon Jul 20 22:01:02 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Sudokusolver
============

Library with a builtin CLI frontend to solve sudoku puzzles using a backtracking algorithm.

In order to solve a sudoku puzzle efficiently Knuth's Algorithm-X is
used after the exact cover problem has been applied to it.

Even this library was actually written to solve sudokus,
you can use the core modules to implement your own solver for any kind of exact cover problems.

Contents:

.. toctree::
   :maxdepth: 2

   usage
   api_reference
