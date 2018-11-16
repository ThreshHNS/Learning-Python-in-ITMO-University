import pygame
from pygame.locals import *
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
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

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.clist = CellList(self.cell_height, self.cell_width, True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list()
            self.clist.update()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self):
        for i in range(self.cell_height):
            for g in range(self.cell_width):
                x = g * self.cell_size + 1
                y = i * self.cell_size + 1
                if self.clist.grid[i][g].is_alive():
                    pygame.draw.rect(self.screen, pygame.Color(
                        'green'), (x, y, self.cell_size-1, self.cell_size-1))
                else:
                    pygame.draw.rect(self.screen, pygame.Color(
                        'white'), (x, y, self.cell_size-1, self.cell_size-1))


class Cell:

    def __init__(self, row, col, state=False):
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self):
        return self.state


class CellList:

    def __init__(self, nrows, ncols, randomize=False):
        self.nrows = nrows
        self.ncols = ncols
        self.randomize = randomize
        if randomize:
            self.grid = [[Cell(r, c, random.randint(0, 1))
                          for c in range(ncols)] for r in range(nrows)]
        else:
            self.grid = [[Cell(r, c) for c in range(ncols)]
                         for r in range(nrows)]

    def get_neighbours(self, cell):
        neighbours = []
        positions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                     (0, 1), (1, 0), (1, -1), (1, 1)]
        for r, c in positions:
            if 0 <= cell.row + r < self.nrows and 0 <= cell.col + c < self.ncols:
                neighbours.append(self.grid[cell.row + r][cell.col + c])
        return neighbours

    def update(self):
        new_clist = deepcopy(self.grid)
        for i in range(self.nrows):
            for j in range(self.ncols):
                neighbours = sum(c.is_alive()
                                 for c in self.get_neighbours(Cell(i, j)))
                if self.grid[i][j].is_alive():
                    if not neighbours in [2, 3]:
                        new_clist[i][j].state = 0
                else:
                    if neighbours == 3:
                        new_clist[i][j].state = 1
        self.grid = new_clist
        return self

    def __iter__(self):
        self.irow = 0
        self.icol = 0
        return self

    def __next__(self):
        if self.irow == self.nrows:
            raise StopIteration
        igrid = self.grid[self.irow][self.icol]
        self.icol += 1
        if self.icol == self.ncols:
            self.icol = 0
            self.irow += 1
        return igrid

    def __str__(self):
        string = '['
        for row in range(self.nrows):
            if row:
                string += ' ['
            else:
                string += '['
            for col in range(self.ncols):
                string += str(int(self.grid[row][col].state))
                if col != self.ncols - 1:
                    string += ', '
            if row != self.nrows - 1:
                string += '],\n'
            else:
                string += ']'
        string += ']'
        return string

    @classmethod
    def from_file(cls, filename):
        filegrid = []
        with open(filename) as file:
            for nrow, line in enumerate(file):
                row = [Cell(nrow, ncol, int(state))
                       for ncol, state in enumerate(line) if state in "01"]
                filegrid.append(row)
        clist = cls(len(filegrid), len(filegrid[0]))
        clist.grid = filegrid
        return clist


if __name__ == '__main__':
    game = GameOfLife(800, 300, 20)
    game.run()
