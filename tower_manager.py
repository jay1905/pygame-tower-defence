import pygame
from tower import Tower

class TowerManager:
  def __init__(self, screen):
    self.screen = screen
    self.towers = []

  def update(self, enemies):
    for tower in self.towers:
      tower.update(self.screen, enemies)

  def create(self, pos, tower_card):
    self.towers.append(Tower(pos[0], pos[1], 18, 18, tower_card.color_base, tower_card.color_top))
