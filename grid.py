import pygame
from config import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_HEIGHT, GRID_WIDTH, GRID_HEIGHT, LIGHT_GRAY

class Grid:
  def __init__(self, screen):
    self.screen = screen
    self.rows = []
    for i in range(GRID_HEIGHT):
        row = []
        for j in range(GRID_WIDTH):
            row.append(0)
        self.rows.append(row)

  def update(self):
    self.draw()

  def draw(self):
    for i in range(GRID_HEIGHT):
      for j in range(GRID_WIDTH):
        rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if self.rows[i][j] == 1:  # If the cell is occupied
          pygame.draw.rect(self.screen, (255, 0, 0), rect)  # Draw a red rectangle
        else:
          pygame.draw.lines(self.screen, LIGHT_GRAY, True,[
            (j * CELL_SIZE, i * CELL_SIZE),
            ((j+1) * CELL_SIZE, i * CELL_SIZE),
            ((j+1) * CELL_SIZE, (i+1) * CELL_SIZE),
            (j * CELL_SIZE, (i+1) * CELL_SIZE)
          ], 1)

  def update_square(self, pos, value):
    self.rows[pos[1]][pos[0]] = value

  def get_square_pos(self, pos):
    x, y = pos
    grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE

    grid_center_x, grid_center_y = (grid_x * CELL_SIZE) + CELL_SIZE / 2, (grid_y * CELL_SIZE) + CELL_SIZE / 2

    if self.rows[grid_y][grid_x] == 0:
      return (grid_center_x, grid_center_y), (grid_x, grid_y)
    return None, None
