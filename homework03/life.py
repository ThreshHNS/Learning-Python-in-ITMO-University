import pygame  # type: ignore
from pygame.locals import *  # type: ignore
import random
from pprint import pprint as pp
from typing import List, Tuple
from copy import deepcopy


class GameOfLife:

    Clist = List[List]
    Neighbours = List[int]
    Cell = Tuple[int, int]

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.clist = self.cell_list()
        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        self.clist = game.cell_list()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:  # type: ignore
                    running = False

            self.draw_grid()

            self.draw_cell_list(self.clist)

            self.clist = self.update_cell_list(self.clist)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize: bool=True) -> Clist:
        """ Создание списка клеток.

        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = []
        if randomize:
            self.clist = [[random.randint(0, 1) for i in range(
                int(self.cell_width))] for j in range(int(self.cell_height))]
        else:
            self.clist = [[0 for i in range(int(self.cell_width))]
                          for j in range(int(self.cell_height))]
        return self.clist

    def draw_cell_list(self, rects: Clist) -> None:
        """ Отображение списка клеток

        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """
        for i in range(len(rects)):
            for g in range(len(rects[i])):
                x = g * self.cell_size + 1
                y = i * self.cell_size + 1
                if rects[i][g]:
                    pygame.draw.rect(self.screen, pygame.Color(
                        'green'), (x, y, self.cell_size - 1, self.cell_size - 1))
                else:
                    pygame.draw.rect(self.screen, pygame.Color(
                        'white'), (x, y, self.cell_size - 1, self.cell_size - 1))

    def get_neighbours(self, cell: Tuple) -> Neighbours:
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []
        positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                     (0, 1), (1, 0), (1, -1), (1, 1)]
        for r, c in positions:
            if 0 <= cell[0] + r < self.cell_height and 0 <= cell[1] + c < self.cell_width:
                neighbours.append(self.clist[cell[0] + r][cell[1] + c])
        return neighbours

    def update_cell_list(self, cell_list: Clist) -> Clist:
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        copy = deepcopy(self.clist)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                neighbours = sum(self.get_neighbours((i, j)))
                if self.clist[i][j]:
                    if not neighbours in [2, 3]:
                        copy[i][j] = 0
                else:
                    if neighbours == 3:
                        copy[i][j] = 1
        self.clist = copy
        return self.clist

if __name__ == '__main__':
    game = GameOfLife(300, 300, 20)
    game.run()
