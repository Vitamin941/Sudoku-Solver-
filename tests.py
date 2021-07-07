import unittest
import solver
import generator
import time

class Tester(unittest.TestCase):

    def empty_count(self,grid):
        result = 0
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == 0:
                    result += 1
        return result

    def test_solve_easy_sudoku(self):
        grid = [
            [5, 0, 0, 0, 8, 6, 0, 0, 1],
            [0, 0, 2, 7, 0, 1, 6 ,0, 0],
            [0, 7, 1, 0, 0, 0, 2, 5, 0],
            [9, 1, 0, 0, 2, 0, 0, 7, 0],
            [3, 0, 0, 1, 4, 5, 0, 0, 6],
            [0, 6, 0, 0, 9, 0, 0, 2, 4],
            [0, 5, 3, 0, 0, 0, 4, 6, 0],
            [0, 0, 8, 9, 0, 3, 5, 0, 0],
            [2, 0, 0, 5, 1, 0, 0, 0, 7]
            ]
        self.assertTrue(solver.solve(grid))
    
    def test_generate_sudoku(self):
        coefs = [x/10 for x in range(10)]
        for coef in coefs:
            with self.subTest(c = coef):
                grid = generator.generate_random_grid(coef)
                self.assertEqual(self.empty_count(grid),int(coef * 81))
    
    def test_not_find_empty(self):
        grid = generator.generate_random_grid(0) # генерируем заполнненый судоку
        self.assertEqual(solver.find_empty_pos(grid),None)

    def test_find_empty(self):
        grid = [
            [0, 0, 5, 3, 0, 0, 0, 0, 0],
            [8, 0, 0, 0, 0, 0, 0, 2, 0],
            [0, 7, 0, 0, 1, 0, 5, 0, 0],
            [4, 0, 0, 0, 0, 5, 3, 0, 0],
            [0, 1, 0, 0, 7, 0, 0, 0, 6],
            [0, 0, 3, 2, 0, 0, 0, 8, 0],
            [0, 6, 0, 5, 0, 0, 0, 0, 9],
            [0, 0, 0 ,4 ,0 ,0 ,0 ,3 ,0],
            [0, 0, 0, 0, 0, 9, 7, 0, 0]
        ]
        self.assertTupleEqual(solver.find_empty_pos(grid),(0,0))
    
    def test_not_valid_col(self):
        grid = [
            [0, 8, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 0, 0, 0, 0, 0, 0], 
            [0, 4, 0, 0, 0, 0, 0, 0, 0], 
            [0, 7, 0, 0, 0, 0, 0, 0, 0], 
            [0, 1, 0, 0, 0, 0, 0, 0, 0], 
            [0, 2, 0, 0, 0, 0, 0, 0, 0], 
            [0, 9, 0, 0, 0, 0, 0, 0, 0], 
            [0, 3, 0, 0, 0, 0, 0, 0, 0],
            [0, 6, 0, 0, 0, 0, 0, 0, 0]
        ]
        poses = [(row,1) for row in range(9)]
        values = [val for val in range(9)]
        for pos in poses:
            for val in values:
                with self.subTest(position = pos,value = val):
                    self.assertFalse(solver.is_valid(grid, val, pos))

    def test_not_valid_row(self):
        grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [1, 4, 3, 5, 7, 8, 2, 9, 6], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        poses = [(3,col) for col in range(9)]
        values = [val for val in range(9)]
        for pos in poses:
            for val in values:
                with self.subTest(position = pos,value = val):
                    self.assertFalse(solver.is_valid(grid, val, pos))

    def test_not_valid_square(self):
        grid = [
            [1, 4, 7, 0, 0, 0, 0, 0, 0],
            [5, 2, 8, 0, 0, 0, 0, 0, 0], 
            [3, 9, 6, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        poses = [(row,col) for col in range(3) for row in range(3)]
        values = [val for val in range(9)]
        for pos in poses:
            for val in values:
                with self.subTest(position = pos,value = val):
                    self.assertFalse(solver.is_valid(grid, val, pos))
    
    def test_valid_pos(self):
        grid = [
            [3, 4, 0, 0, 0, 2, 0, 0, 8],
            [6, 0, 8, 0, 0, 0, 0, 9, 0],
            [0, 1, 2, 6, 0, 0, 0, 3, 0],
            [0, 3, 0, 0, 9, 1, 0, 0, 7], 
            [0, 0, 0, 5, 0, 7, 0, 0, 0], 
            [0, 6, 0, 0, 0, 4, 0, 8, 0], 
            [1, 0, 0, 7, 0, 0, 5, 0, 6], 
            [0, 8, 9, 0, 0, 0, 0, 0, 0], 
            [4, 5, 0, 1, 0, 0, 0, 0, 0]
        ]
        pos = (0,2)
        val = 5
        self.assertTrue(solver.is_valid(grid,val,pos))

if __name__ == "__main__":
    unittest.main()