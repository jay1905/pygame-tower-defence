import pygame
from enemy import Enemy

class Level:
  def __init__(self):
    self.spawn_locations = [(0,100),(0,200),(0,300),(0,400),(0,500)]
    self.spawn_points = [0,1,2,3,4,3,2,1,0,1]
    self.enemy_types = ['n','n','n','n','n','n','n','n','n','n']
    self.enemy_count = 0
    self.spawn_speed = 60
    self.can_spawn = 0
