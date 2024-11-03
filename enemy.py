import pygame
import math
from pathfinding import a_star_search, heuristic, reconstruct_path
from config import CELL_SIZE

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Enemy:
  def __init__(self, pos, width, height, speed, value=50):
    self.x = pos[0]
    self.y = pos[1]
    self.width = width
    self.height = height
    self.speed = speed
    self.value = value
    self.arrived = False
    self.goal = (39, pos[1] // CELL_SIZE)
    self.health = 10
    self.path = []
    self.rect = pygame.Rect(self.x - width/2, self.y - height/2, width, height)

  def draw(self, screen):
    pygame.draw.rect(screen, (0, 255, 255), self.rect)
    self.draw_path(screen)

  def move(self):
    if self.path:  # If there is a path
      next_cell = self.path[0]  # The next cell to move to
      next_pixel = (next_cell[0] * CELL_SIZE + CELL_SIZE // 2, next_cell[1] * CELL_SIZE + CELL_SIZE // 2)

      # Calculate the direction to the next cell
      dx = next_pixel[0] - self.x
      dy = next_pixel[1] - self.y
      distance = math.sqrt(dx**2 + dy**2)

      # Normalize the direction and scale by the enemy's speed
      dx /= distance
      dy /= distance
      dx *= self.speed
      dy *= self.speed

      # Move the enemy
      self.x += dx
      self.y += dy
      self.rect.x = self.x - self.width / 2
      self.rect.y = self.y - self.height / 2

      # If the enemy has reached the next cell, remove it from the path
      if math.hypot(self.x - next_pixel[0], self.y - next_pixel[1]) < self.speed:
        self.path.pop(0)

    # If the enemy has reached the goal or is out of bounds, return True
    if not self.path or self.x < 0 or self.y < 0 or self.x > SCREEN_WIDTH or self.y > SCREEN_HEIGHT:
      self.arrived = True

  def update(self, screen):
    self.draw(screen)
    self.move()

  def calculate_path(self, rows):
    start = (int(self.x // CELL_SIZE), int(self.y // CELL_SIZE))
    came_from, cost_so_far = a_star_search(rows, start, self.goal)
    path = reconstruct_path(came_from, start, self.goal)
    self.path = path

  def draw_path(self, screen):
    for i in range(len(self.path) - 1):
      start = self.path[i]
      end = self.path[i + 1]
      start_pixel = (start[0] * CELL_SIZE + CELL_SIZE // 2, start[1] * CELL_SIZE + CELL_SIZE // 2)
      end_pixel = (end[0] * CELL_SIZE + CELL_SIZE // 2, end[1] * CELL_SIZE + CELL_SIZE // 2)
      pygame.draw.line(screen, (0, 255, 0), start_pixel, end_pixel)
