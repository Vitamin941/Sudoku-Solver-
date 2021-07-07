from random import randint,sample

# изначально заполненный судоку 
START_GRID = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [2, 3, 4, 5, 6, 7, 8, 9 ,1],
    [5, 6, 7, 8, 9, 1, 2, 3, 4],
    [8, 9, 1, 2, 3, 4, 5, 6, 7],
    [3, 4, 5, 6, 7, 8, 9, 1, 2],
    [6, 7, 8, 9, 1, 2, 3, 4, 5],
    [9, 1, 2, 3, 4, 5, 6, 7, 8]
]

 
class Matrix():

    def __init__(self,grid=START_GRID[:],n=3):
        self.grid = grid[:]
        self.N = n # длина стороны квадрата [3 X 3]

    def transporning(self):
        '''
        Транспонирует матрицу

        return изменяет матрицу на месте, поэтому ничего не возвращаем
        '''
        self.grid = [list(l) for l in zip(*self.grid)]
    
    def get_two_random_nums(self):
        '''
        Возвращает два случайных(попарно различных) значения в пределах [0;N), где N - размер судоку (3 X 3)
        '''
        num1 = randint(0,self.N - 1)
        num2 = randint(0,self.N - 1)
        while num2 == num1:
            num2 = randint(0,self.N - 1)
    
        return num1, num2

    def swap_rows_in_square(self):
        '''
        Переставляет строки в пределах одного квадрата
        (квадрат и строки выбираются случайно)

        return изменяет матрицу на месте, поэтому ничего не возвращаем
        '''
        square = randint(0,self.N - 1) # получение случайного номера для квадрата 
        row_in_square_1, row_in_square_2 = Matrix.get_two_random_nums(self)  

        row_1_in_table = self.N * square + row_in_square_1
        row_2_in_table = self.N * square + row_in_square_2

        self.grid[row_1_in_table], self.grid[row_2_in_table] = self.grid[row_2_in_table], self.grid[row_1_in_table]



    def swap_cols_in_square(self):
        '''
        Переставляет столбцы в пределах одного квадрата
        (квадрат и столбцы выбираются случайно)

        return изменяет матрицу на месте, поэтому ничего не возвращаем
        '''
        Matrix.transporning(self)
        Matrix.swap_rows_in_square(self)
        Matrix.transporning(self)

    def swap_big_rows(self):
        '''
        Переставляет ряды 3 X 3 (квадраты) между собой в рамках строк
        (строки для перестановки выбираются случайно)
        '''
        row1, row2 = Matrix.get_two_random_nums(self) # получение двух случайных разных строк
  
        for i in range(self.N):
             N1, N2 = row1 * self.N + i, row2 * self.N + i
             self.grid[N1], self.grid[N2] = self.grid[N2], self.grid[N1]

    def swap_big_cols(self):
        '''
        Переставляет ряды 3 X 3 (квадраты) между собой в рамках столбцов
        (столбцы для перестановки выбираются случайно)
        '''
        Matrix.transporning(self)
        Matrix.swap_big_rows(self)
        Matrix.transporning(self)

    def mix_board(self,mix_num=25):
        '''
        Используется для того,чтобы случайным образом
        перемешать матрицу используя функции заданные выше

        param:
            mix_num - число задающее количество вызовов других функции 
                      и соответственно качество перемешивания матрицы
        return: перемешанная матрица
        '''
        defs = [
            "self.swap_cols_in_square()",
            "self.swap_rows_in_square()",
            "self.swap_big_rows()",
            "self.swap_big_cols()"
        ]
    
        for i in range(mix_num):
            def_id = randint(0,len(defs) - 1)
            eval(defs[def_id])


    def clear_some_elements(self,coef_empty=0.65):
        '''
            Удаляет некоторые элементы из судоку
            При желании можно изменить коэффициент на который будет умножаться 81 (число элементов в судоку 3 X 3)

            param: self - объект класса Matrix 
                   coef_empty - коэффициент очищенных элементов.
        '''
        elements = self.N ** 4
        side = self.N ** 2
        empties = int(elements * coef_empty)
        for index in sample(range(elements),empties):
            self.grid[index // side][index % side] = 0
    
    def get_grid(self):
        '''
        Возвращает матрицу
        '''
        return self.grid
    

    
def generate_random_grid(coef_hard=0.65):
    '''
    Создаёт матрицу,применяет к ней операции, реализованные в классе Matrix
    
    param: coef_hard - коэф. сложности где 0 - решёный судоку, 1 - пустой судоку("самый сложный")
    return: случайный судоку, готовый к разрешению
    '''
    matr = Matrix()
    matr.mix_board()
    matr.clear_some_elements(coef_hard)
    return matr.get_grid()

if __name__ == '__main__':
    m = Matrix()
    m.mix_board()
    m.clear_some_elements()
    print(m.get_grid())