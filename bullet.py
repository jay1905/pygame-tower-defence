import pygame
import math

class Bullet:
  def __init__(self, pos, damage, enemy):
    self.x = pos[0]
    self.y = pos[1]
    self.radius = 4
    self.speed = 5
    self.enemy = enemy
    self.damage = damage
    self.direction = (0,0)
    self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

  def draw(self, screen):
    pygame.draw.circle(screen, 'red', (self.x, self.y), self.radius)

  def move(self):
    self.direction = self.get_direction()
    self.x += self.direction[0] * self.speed
    self.y += self.direction[1] * self.speed
    self.rect.x = self.x - self.radius
    self.rect.y = self.y - self.radius

  def update(self, screen):
    self.draw(screen)
    self.move()

    if self.rect.colliderect(self.enemy.rect):
      self.enemy.health -= self.damage
      return True
    
    return False

  def get_direction(self):
    dx = self.enemy.x - self.x
    dy = self.enemy.y - self.y
    length = math.sqrt(dx * dx + dy * dy)
    if length > 0:
        dx /= length
        dy /= length
    return dx, dy