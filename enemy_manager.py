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
    self.enemy_spawn_times = []
    self.enemy_count = 0
    self.spawn_speed = 0
    self.level_time = 0
    self.can_spawn = 0
    self.time = 0
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

  def update_enemy_spawner(self, spawn_points, enemy_types, spawn_speed, enemy_spawn_times, level_time):
    self.enemy_spawn_times = enemy_spawn_times
    self.level_time = level_time
    self.spawn_points = spawn_points
    self.enemy_types = enemy_types
    self.spawn_speed = spawn_speed

  def spawn(self):
    # Implement the logic to spawn the next enemy
    # every second
    self.time += 1
    if self.time > 60:
      self.can_spawn += 1
      self.time = 0

    if self.can_spawn in self.enemy_spawn_times and self.spawn_points and self.enemy_types:
    # if self.can_spawn >= self.spawn_speed:
      print("Spawning enemy {self.enemy_count}", self.enemy_spawn_times[0])
      enemy = Enemy(self.spawn_locations[self.spawn_points[0]], 15, 15, 2)
      enemy.calculate_path(self.rows)

      self.enemies.append(enemy)
      self.spawn_points.remove(self.spawn_points[0])
      self.enemy_types.remove(self.enemy_types[0])
      self.enemy_spawn_times.remove(self.enemy_spawn_times[0])
    # else:
      # self.can_spawn += 1

  def recalaulate_path(self):
    for enemy in self.enemies[:]:
      enemy.calculate_path(self.rows)

  def spawn_wave(self, wave):
    # Implement the logic to spawn the next wave of enemies
    self.can_spawn = 0
    print(f"Spawning wave {wave}")






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
