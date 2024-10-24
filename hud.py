import pygame
from config import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, HUD_BACKGROUND_COLOR, TOWER_WIDTH
from tower_card import TowerCard

class Hud:
  def __init__(self, screen):
    self.screen = screen
    self.font = pygame.font.Font(None, 36)
    self.background = pygame.Rect(0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200)
    self.selected_card = None
    self.coins = 120
    self.tower_cards = [
      TowerCard((10, SCREEN_HEIGHT - 200 + 10), (0, 255, 255), (0, 200, 255), 50),
      TowerCard((100, SCREEN_HEIGHT - 200 + 10), (50, 250, 50), (50, 200, 50), 100)]

  def update(self):
    self.draw()

  def update_coins(self, value):
    self.coins += value

  def buy_tower(self, cost):
    if self.coins >= cost:
      return True
    return False

  def draw_rounded_rect(self, rect, color, radius):
    pygame.draw.rect(self.screen, color, rect, border_radius=radius)

  def draw(self):
    # Draw the HUD background
    pygame.draw.rect(self.screen, HUD_BACKGROUND_COLOR, self.background)

    coins_text = self.font.render(f"Coins: {self.coins}", True, (255, 255, 255))
    coins_text_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 180))
    self.screen.blit(coins_text, coins_text_rect)

    # Draw the tower cards
    for tower in self.tower_cards:
      tower.draw(self.screen)
    # Draw the selected tower following the mouse
    if self.selected_card:
      pos = pygame.mouse.get_pos()
      x = pos[0] - TOWER_WIDTH // 2
      y = pos[1] - TOWER_WIDTH // 2
      tower_rect = pygame.Rect(x, y, TOWER_WIDTH, TOWER_WIDTH)
      pygame.draw.rect(self.screen, self.selected_card.color_base, tower_rect)
      pygame.draw.circle(self.screen, self.selected_card.color_top, (pos[0], pos[1]), TOWER_WIDTH // 2)
       # range circle
      pygame.draw.circle(self.screen, (50, 50, 100), (pos[0], pos[1]), self.selected_card.range, 1)

  def handle_click(self, pos):
    for tower in self.tower_cards:
      card_x, card_y = tower.position
      card_rect = pygame.Rect(card_x, card_y, tower.width, tower.height)
      if card_rect.collidepoint(pos):
        if self.selected_card:
            self.selected_card.selected = False
        if self.selected_card == tower:
            self.selected_card = None
        else:
          tower.selected = True
          self.selected_card = tower
        break
