from generator import generate_random_grid


def solve(board):
    '''
    Главная функция, которая решает судоку
    Реализует алгоритм поиска с возратом.

    param: board - таблица судоку

    return True если судоку решён
    '''
    empty_pos = find_empty_pos(board) 
    if not empty_pos:
        return True
    else:
        row, col = empty_pos

    for i in range(1,10):
        if is_valid(board,i,(row,col)):
            board[row][col] = i  # распологаем числа в таблице

            if solve(board): # и заходим на следующую свободную клетку
                return True

            board[row][col] = 0 # если решение не было найдено обнуляем клетку 

    return False  
            
def print_board(board):
    '''
    Красивый вывод на консоль,
    удобно осматривать и отлаживать
    
    param: board - таблица судоку
    '''
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("-------------------")
        
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print("|" , end="")
            
            if j == 8:
                print(board[i][j])
            else:
                print(board[i][j],end=" ")
 
def find_empty_pos(board):
    '''
    Поиск ещё не открытого элемента (обозначен как 0)

    param: board - таблица судоку

    return: строка и столбец соотвественно. 
    '''
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i , j) 
    # возращаем None если все ячейки имеют значение(т.е. судоку решён)            
    return None 

def is_valid(board,num : int,pos : tuple):
    '''
    Проверяет возможно ли разместить 
    в конкректной позиции конкретное число

    Содержит внутренние функции на проверку 
    строки, столбца и квадрата соответственно.

    params:
        board - таблица судоку
        num - число, подозрительное на размещение
        pos - позиция (строка,столбец) в которую мы хотим разместить число.

    return: bool значение 
    '''

    def is_valid_row():
        '''
        Проверяет возможно ли разместить число в данной строке

        return: bool значение
        '''
        row_index = pos[0]

        for index in range(len(board)):
            if board[row_index][index] == num:
                return False
        return True

    def is_valid_col():
        '''
        Проверяет возможно ли разместить число в данном столбце

        return: bool значение
        '''
        col_index = pos[1]

        for index in range(len(board[0])):
            if board[index][col_index] == num:
                return False
        return True

    def is_valid_square():
        '''
        Проверяет возможно ли разместить число в данном квадрате

        return: bool значение 
        '''
        box_x = pos[0] // 3 # находим квадрат в котором нахомдится число по стобцу
        box_y = pos[1] // 3 # находим квадрат в котором нахомдится число по строке

        for row in range(box_x * 3 , box_x * 3 + 3): 
            for col in range(box_y * 3, box_y * 3 + 3):
                if board[row][col] == num:
                    return False
        return True
    
    if is_valid_col() and is_valid_row() and is_valid_square(): #Если всё условия выполнены число можно разместить
        return True
    else:
        return False

if __name__ == "__main__":
    board = generate_random_grid()
    print_board(board)
    solve(board)
    print()
    print_board(board)
