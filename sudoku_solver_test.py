#!/usr/bin/env python
# encoding: utf-8
import unittest

import importer
import solver


class SudokuSolverTest(unittest.TestCase):
    def test_solve_empty_example(self):
        fixed_candidates = importer.imp_candidates('example-empty.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)

    def test_solve_complete_example(self):
        fixed_candidates = importer.imp_candidates('example-complete.csv')
        solution = solver.solve(fixed_candidates)
        self.assertFalse(solution)

    def test_solve_example_1(self):
        fixed_candidates = importer.imp_candidates('example1.csv')
        solution = solver.solve(fixed_candidates)
        self.assertFalse(solution)

    def test_solve_example_1(self):
        fixed_candidates = importer.imp_candidates('example2.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)

    def test_solve_example_2(self):
        fixed_candidates = importer.imp_candidates('example2.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)

    def test_solve_example_3(self):
        fixed_candidates = importer.imp_candidates('example3.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)

    def test_solve_example_4(self):
        fixed_candidates = importer.imp_candidates('example4.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)

    def test_solve_example_5(self):
        fixed_candidates = importer.imp_candidates('example5.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)

    def test_solve_example_6(self):
        fixed_candidates = importer.imp_candidates('example6.csv')
        solution = solver.solve(fixed_candidates)
        self.assertTrue(solution)


if __name__ == '__main__':
    unittest.main()
