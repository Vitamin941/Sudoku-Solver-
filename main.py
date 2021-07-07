import pygame
import time
from generator import generate_random_grid
from solver import is_valid, find_empty_pos

pygame.init()

WIDTH = 540
HEIGHT = 600
GAME_WIDTH = 540
GAME_HEIGHT = 540
GAP = WIDTH / 9
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill((255, 255, 255))
MAIN_FNT = pygame.font.SysFont("comicsans", 40)
SUP_FNT = pygame.font.SysFont("comicsans", 35)


class Grid:
    '''
    Класс реализующий модель судоку 
    '''

    def __init__(self, board, row=9, col=9):
        '''
        cols - число столбцов
        rows - число строк
        start_pos - изначальная сгенерированная матрица
        model - представление судоку в виде вложенных списков
        cubes - представление судоку в виде класса ячейки
        selected_pos - позиция,выбранная в данный момент
        '''
        self.cols = col
        self.rows = row
        self.start_pos = board
        self.model = self.start_pos
        self.cubes = [[Cube(self.start_pos[i][j], i, j) for j in range(self.rows)] for i in range(self.cols)]
        self.selected_pos = None

    def reset_grid(self):
        '''
        Возвращет судоку к изначально сгенеированному положению,
        обновляет как графическое представление так и модель
        '''
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].set_value(self.start_pos[i][j])
        self.update_model()
        pygame.display.update()

    def update_model(self):
        '''
        Обновляет системное отображаение судоку, 
        получая информацию из графического интерфейса

        системное отображение - список списков
        '''
        self.model = [[self.cubes[i][j].value for j in range(self.rows)] for i in range(self.cols)]

    def place(self, val: int):
        '''
        Размещает значение в заданной клетке, 
        обновляет как графическое представление так и модель 

        param: val - значение

        return bool значение
        '''

        if not self.selected_pos:
            return

        row, col = self.selected_pos

        if self.cubes[row][col].value == 0 and is_valid(self.model, val, self.selected_pos):
            self.cubes[row][col].set_value(val)
            self.update_model()
            return True
        return False

    def delete(self):
        '''
        Удаляет значение с выбранной клетки

        return: bool значение  
        '''
        row, col = self.selected_pos
        if self.cubes[row][col] != 0 and self.start_pos[row][col] == 0:
            self.cubes[row][col].set_value(0)
            self.update_model()
            return True
        return False

    def click(self, pos: tuple):
        '''
        Считывает положение мыши и приводит его к значению (row, col)

        pos - положение мыши

        return (row,col) - (строка,столбец)
        '''
        if pos[0] < GAME_HEIGHT and pos[1] < GAME_WIDTH:
            row = pos[1] // GAP
            col = pos[0] // GAP
            return (int(row), int(col))
        else:
            return None

    def is_solved(self):
        '''
        Проверяет решён ли судоку

        return: bool значение 
        '''
        for row in range(self.rows):
            for col in range(self.cols):
                if self.model[row][col] == 0:
                    return False
        return True

    def select(self, pos: tuple):
        '''
        Помечает клетку таблицы (row, col) как выбранную

        param: pos (row,col)

        return: bool значение
        '''
        row, col = pos
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected_pos = (row, col)

    def draw_lines(self):
        '''
        Отрисовывает линии игрового поля
        '''

        for i in range(self.rows + 1):
            thick = 1
            if i % 3 == 0 and i != 0:
                thick = 4  # толщина линии

            pygame.draw.line(SCREEN, (0, 0, 0), (0, i * GAP), (GAME_WIDTH, i * GAP),
                             thick)  # отрисовка горизонтальных линий
            pygame.draw.line(SCREEN, (0, 0, 0), (i * GAP, 0), (i * GAP, GAME_HEIGHT),
                             thick)  # отрисовка вертикальных линий

    def draw(self):
        '''
        Главная функция отрисовки,полностью реализует отображение игрового окна 
        '''
        self.draw_lines()

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw()

        self.draw_selected()

    def draw_selected(self):
        '''
        Отмечает в графическом интерфейсе выбранную клетку 
        '''
        thick = 4

        if not self.selected_pos:
            return

        pos_x = self.selected_pos[1] * GAP
        pos_y = self.selected_pos[0] * GAP

        pygame.draw.rect(SCREEN, (0, 0, 255), (pos_x, pos_y, GAP, GAP), 3)

    def solve_gui(self):
        '''
        Главная функция решателя судоку в графическом интерфейсе пользователя
        реализует алгоритм поиска с возвратом 

        return: bool значение
        '''
        self.update_model()
        find_pos = find_empty_pos(self.model)

        if not find_pos:
            return True
        else:
            row, col = find_pos

        for i in range(1, 10):
            if (is_valid(self.model, i, find_pos)):
                self.model[row][col] = i
                self.cubes[row][col].set_value(i)
                self.cubes[row][col].draw_change(good_spot=True)
                self.update_model()
                pygame.time.wait(100)
                pygame.display.update()

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set_value(0)
                self.cubes[row][col].draw_change(good_spot=False)
                self.update_model()
                pygame.time.wait(100)
                pygame.display.update()

        return False


class Cube:
    '''
    Класс реализующий модель одного числа в таблице судоку
    '''

    def __init__(self, val: int, row: int, col: int):
        '''
        value - значение в клетке
        row - строка 
        col - столбец
        selected - проверяет выбрана ли эта клетка
        '''
        self.value = val
        self.row = row
        self.col = col
        self.selected = False

    def draw(self):
        '''
        Отрисовывает значение находящееся в клетке
        '''
        pos_x = GAP * self.col
        pos_y = GAP * self.row
        if self.value != 0:
            text = MAIN_FNT.render(str(self.value), 1, (0, 0, 0))
            SCREEN.blit(text, (pos_x + 20, pos_y + 15))

    def draw_change(self, good_spot=False):
        """
        Отрисовывает процесс изменения значение клетки
        Используется только для графического решателя

        param: good_spot - bool значение, проверяет значение в конктреной клетке
        может ли является решением
        """
        pos_x = GAP * self.col
        pos_y = GAP * self.row
        thick = 4

        pygame.draw.rect(SCREEN, (255, 255, 255), (thick + pos_x, thick + pos_y, GAP - thick, GAP - thick), 0)

        if good_spot:
            pygame.draw.rect(SCREEN, (0, 255, 0), (pos_x, pos_y, GAP, GAP), 3)
        else:
            pygame.draw.rect(SCREEN, (255, 0, 0), (pos_x, pos_y, GAP, GAP), 3)

        if self.value == 0:
            return

        text = MAIN_FNT.render(str(self.value), 1, (0, 0, 0))
        SCREEN.blit(text, (pos_x + 20, pos_y + 15))

    def set_value(self, val: int):
        '''
        Стандартный сеттер для значения клетки

        val - новое значение
        '''
        self.value = val


def time_format(secs: float):
    '''
    Приводит секунды в формат времени 
    минуты:секунды
    
    param: secs  - секунды

    return: строка в формате минуты:секунды 
    '''
    sec = secs % 60
    mins = secs // 60

    if sec < 10:
        sec = "0" + str(sec)
    if mins < 10:
        mins = "0" + str(mins)

    mat = " " + str(mins) + ":" + str(sec)
    return mat


def redraw_window(board: Grid, time: int, strikes: int):
    '''
    Обновление игрового окна

    param:
        board: таблица судоку
        time: время прошедшее с начала запуска
        strikes: кол-во ходов
    '''
    SCREEN.fill((255, 255, 255))

    # Отрисовка времени
    time_text = SUP_FNT.render("Время: " + time_format(time), 1, (0, 0, 0))
    SCREEN.blit(time_text, (360, 560))

    # Отрисовка кол-ва ходов
    strikes_text = SUP_FNT.render("X: " + str(strikes), 1, (0, 0, 0))
    SCREEN.blit(strikes_text, (0, 560))

    board.draw()
    pygame.display.update()


def main_loop():
    '''
    Главный игровый цикл
    '''
    pygame.display.set_caption("Sudoku")
    running = True
    grid = Grid(generate_random_grid())
    start_time = time.time()
    strikes = 0
    while running:
        in_game_time = round(time.time() - start_time)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                key = 0
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9

                if event.key == pygame.K_DELETE:
                    if grid.delete():
                        strikes += 1

                if event.key == pygame.K_RETURN:  # enter сбрасывает игровое поле до начального состояния
                    grid.reset_grid()

                if event.key == pygame.K_SPACE:  # если был нажат space вызываем решатель
                    grid.reset_grid()
                    grid.solve_gui()

                if key != 0:
                    if grid.place(key):
                        strikes += 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = grid.click(pos)
                if clicked:
                    grid.select(clicked)
                    print(f"selected: [{clicked[0]},{clicked[1]}]")

            if grid.is_solved():
                print(f"sudoku is solved: {strikes}")

        redraw_window(grid, in_game_time, strikes)
        pygame.display.update()


main_loop()
pygame.display.quit()
pygame.quit()
