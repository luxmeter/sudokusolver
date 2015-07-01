#!/usr/bin/env python
# encoding: utf-8
import unittest

from sudoku import importer
from sudoku import solver


class SudokuSolverTest(unittest.TestCase):
    def test_solve_empty_example(self):
        fixed_candidates = importer.imp_candidates(
            'sudoku/test/resources/example-empty.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)

    def test_solve_complete_example(self):
        fixed_candidates = importer.imp_candidates(
            'sudoku/test/resources/example-complete.csv')
        solution = solver.solve(fixed_candidates)
        self.assertFalse(solution)

    def test_solve_example_1(self):
        fixed_candidates = importer.imp_candidates(
            'sudoku/test/resources/example1.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)

    def test_solve_example_2(self):
        fixed_candidates = importer.imp_candidates(
            'sudoku/test/resources/example2.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)

    def test_solve_example_3(self):
        fixed_candidates = importer.imp_candidates(
            'sudoku/test/resources/example3.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)

    def test_solve_example_4(self):
        fixed_candidates = importer.imp_candidates(
            'sudoku/test/resources/example4.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)

    def test_solve_example_5(self):
        fixed_candidates = importer.imp_candidates(
            'sudoku/test/resources/example5.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)

    def test_solve_example_6(self):
        fixed_candidates = importer.imp_candidates(
            'sudoku/test/resources/example6.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)


if __name__ == '__main__':
    unittest.main()
