import pygame
from enemy import Enemy

class EnemyManager:
  def __init__(self, screen, hud):
    self.screen = screen
    self.hud = hud
    self.enemies = []
    self.spawn_locations = [(0,100),(0,200),(0,300),(0,400),(0,500)]
    self.spawn_points = []
    self.enemy_types = []
    self.enemy_count = 0
    self.spawn_speed = 0
    self.can_spawn = 0
    self.rows = []

  def update(self):
    for enemy in self.enemies[:]:
      if enemy.arrived:
        self.hud.update_health(-1)
        self.enemies.remove(enemy)
        continue

      if enemy.health <= 0:
        self.hud.update_coins(enemy.value)
        self.enemies.remove(enemy)
        continue

      enemy.update(self.screen)

    if self.enemy_types:
      self.spawn()

  def update_enemy_spawner(self, spawn_points, enemy_types, spawn_speed):
    self.spawn_points = spawn_points
    self.enemy_types = enemy_types
    self.spawn_speed = spawn_speed

  def spawn(self):
    if self.can_spawn >= self.spawn_speed:
      self.can_spawn = 0
      enemy = Enemy(self.spawn_locations[self.spawn_points[0]], 15, 15, 2)
      enemy.calculate_path(self.rows, (39,3))

      self.enemies.append(enemy)
      self.spawn_points.remove(self.spawn_points[0])
      self.enemy_types.remove(self.enemy_types[0])
    else:
      self.can_spawn += 1

  def recalaulate_path(self):
    for enemy in self.enemies[:]:
      enemy.calculate_path(self.rows, (39,3))









       #collide logic  

    #  if enemy.rect.colliderect(player):
    #   # enemies.remove(enemy)
    #   if player.right >= enemy.rect.left and player.right <= enemy.rect.left + 5:
    #     player.right = enemy.rect.left
    #   if player.left <= enemy.rect.right and player.left >= enemy.rect.right - 5:
    #     player.left = enemy.rect.right
    #   if player.top <= enemy.rect.bottom and player.top >= enemy.rect.bottom - 5:
    #     player.top = enemy.rect.bottom
    #   if player.bottom >= enemy.rect.top and player.bottom <= enemy.rect.top + 5:
    #     player.bottom= enemy.rect.top
