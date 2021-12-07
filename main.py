import pygame
from queue import PriorityQueue, Queue
pygame.init()

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Dijkstra Path Finder Algorithm with PyGame")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:

    def __init__(self, row, col, width, total_rows, name):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbor = []
        self.width = width
        self.total_rows = total_rows
        self.value = float('inf')
        self.name = name

    def get_position(self):
        return self.row, self.col

    def is_white(self):
        return self.color == WHITE

    def is_closed(self):
        return self.color == RED

    def is_barrier(self):
        return self.color == BLACK

    def is_open(self):
        return self.color == GREEN

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def reset(self):
        self.color = WHITE

    def get_name(self):
        return self.name

    def set_closed(self):
        self.color = RED

    def set_start(self):
        self.color = ORANGE

    def set_end(self):
        self.color = TURQUOISE

    def set_barrier(self):
        self.color = BLACK

    def set_open(self):
        self.color = GREEN

    def set_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(
            WIN, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbor = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbor.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbor.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbor.append(grid[self.row][self.col - 1])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbor.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False


def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    pygame.display.update()


def create_grid(width, rows):
    count = 0
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows, count)
            grid[i].append(node)
            count += 1
    return grid


def reconstruct_path(came_from, current, draw, start):
    while current in came_from:
        if current == start:
            return True
        current = came_from[current]
        current.set_path()
        draw()


def algorithm(draw, start, end):

    unvisited_que = Queue()
    start.set_value(0)
    unvisited_que.put(start)

    came_from = {start: start}

    run = True
    current = start
    while run == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = unvisited_que.get()

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            end.set_end()
            start.set_start()
            return True

        for neighbor in current.neighbor:
            if neighbor.is_white() or neighbor.is_end():
                if (current.get_value() + 1) < neighbor.get_value():
                    came_from[neighbor] = current
                    neighbor.set_value(current.get_value() + 1)
                    neighbor.set_open()
                unvisited_que.put(neighbor)

        print("Node: " + str(current.get_name()) +
              " - distance from start:" + str(current.get_value()))

        if current != start:
            current.set_closed()

        draw()

    return False


def main(win, width):
    ROWS = 100

    grid = create_grid(width, ROWS)

    run = True

    start = None
    end = None

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT MOUSE BUTTON
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.set_start()

                elif not end and node != start:
                    end = node
                    end.set_end()

                elif node != end and node != start:
                    node.set_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT MOUSE BUTTON
                pos = pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width),
                              start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid(width, ROWS)

    pygame.quit()


main(WIN, WIDTH)
