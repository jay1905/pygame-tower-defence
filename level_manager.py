import pygame
from level import Level
from config import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_HEIGHT, GRID_WIDTH, GRID_HEIGHT

class LevelManager:
  def __init__(self):
    self.current_level = 0
    self.levels = []

  def update(self):
    for level in self.levels[:]:
      level.update()

  def load_level(self,level) :
    print('load level')

  def create(self, data):
    for d in data[:]:
      level = Level(d[1])
      self.levels.append(level)
      print('create level')
