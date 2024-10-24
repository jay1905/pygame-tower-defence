import pygame
from bullet import Bullet

class Tower:
  def __init__(self, x, y, width, height, color_base, color_top):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.color_base = color_base
    self.color_top = color_top
    self.bullets = []
    self.range = 60
    self.fire_rate = 60
    self.fire_counter = 30
    self.can_fire = True
    self.rect = pygame.Rect(x - width/2, y - height/2, width, height)

  def draw(self, screen):
    pygame.draw.rect(screen, self.color_base, self.rect)
    pygame.draw.circle(screen, self.color_top, (self.x, self.y), self.width // 2)

    # range circle
    pygame.draw.circle(screen, (0, 0, 100), (self.x, self.y), self.range, 1)

    for b in self.bullets[:]:
      if b.update(screen):
        self.bullets.remove(b)
      
  def shoot(self, enemy):
    b = Bullet((self.x, self.y), 3, enemy)
    self.bullets.append(b)

  def update(self, screen, enemies):
    self.draw(screen)

    if self.fire_counter < 0:
      self.fire_counter = self.fire_rate
      self.can_fire = True
    elif self.can_fire == False:
      self.fire_counter -= 1

    if self.can_fire:
      for enemy in enemies:
        dx = self.x - enemy.x
        dy = self.y - enemy.y
        distance = (dx**2 + dy**2)**0.5
        if distance <= self.range:
          self.shoot(enemy)
          self.can_fire = False
