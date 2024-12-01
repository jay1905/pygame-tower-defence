import pygame
from config import (CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, HUD_BACKGROUND_COLOR, TOWER_WIDTH,
                    LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT, LOADING_BAR_COLOR, LOADING_BAR_BG_COLOR, LOADING_BAR_POSITION,
                    SEGMENT_WIDTH, BAR_HEIGHT, BAR_COLORS, BAR_BG_COLOR, BAR_POSITION
                  )
from tower_card import TowerCard

CLIP_RECT = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50, SCREEN_WIDTH // 2, 50)

class Hud:
  def __init__(self, screen):
    self.screen = screen
    self.font = pygame.font.Font(None, 36)
    self.background = pygame.Rect(0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200)
    self.selected_card = None
    self.coins = 120
    self.health = 100
    self.game_over = False
    self.levels = []
    self.current_level = 0
    self.enemy_manager = None
    self.background_layer = pygame.Surface((SCREEN_WIDTH // 2 , 50))
    self.bar_movement_speed = 1
    self.tower_cards = [
      TowerCard((10, SCREEN_HEIGHT - 200 + 10), (0, 255, 255), (0, 200, 255), 50),
      TowerCard((100, SCREEN_HEIGHT - 200 + 10), (50, 250, 50), (50, 200, 50), 100)]

  def update_health(self, value):
    self.health += value
    if self.health <= 0:
      self.game_over = True

  def reset(self):
    self.coins = 120
    self.health = 1
    self.game_over = False

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

    health_text = self.font.render(f"Health: {self.health}", True, (255, 255, 255))
    health_text_rect = health_text.get_rect(center=(SCREEN_WIDTH // 2 + (SCREEN_WIDTH // 2) // 2, SCREEN_HEIGHT - 180))
    self.screen.blit(health_text, health_text_rect)

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
     # Set the clipping region
    self.screen.set_clip(CLIP_RECT)
    self.background_layer.fill((200, 200, 200))  # Fill with a background color
    self.screen.blit(self.background_layer, (SCREEN_WIDTH // 4, SCREEN_HEIGHT - 50))
    self.draw_moving_bar()
    # Reset the clipping region
    self.screen.set_clip(None)

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

  def draw_moving_bar(self):
    # Draw the background of the bar
    pygame.draw.rect(self.screen, BAR_BG_COLOR, (*BAR_POSITION, SEGMENT_WIDTH * len(self.levels), BAR_HEIGHT))
    
    # Draw each color segment
    for i, level in enumerate(self.levels):
      segment_start = BAR_POSITION[0] + i * SEGMENT_WIDTH
      pygame.draw.rect(self.screen, level.color, (segment_start, BAR_POSITION[1], SEGMENT_WIDTH, BAR_HEIGHT))
        # Draw the wave count text
      wave_text = self.font.render(f"Wave {i + 1}", True, (255, 255, 255))
      wave_text_rect = wave_text.get_rect(center=(segment_start + SEGMENT_WIDTH // 2, BAR_POSITION[1] + BAR_HEIGHT // 2))
      self.screen.blit(wave_text, wave_text_rect)

    # Check if the segment reaches the start of the mask
    if BAR_POSITION[0] + (self.current_level * SEGMENT_WIDTH) <= SCREEN_WIDTH // 4:
      # Spawn the next wave
      self.current_level += 1
      self.enemy_manager.spawn_wave(self.current_level)
      self.set_bar_moving_spead(self.levels[self.current_level].level_time)
    # Move the bar from right to left
    BAR_POSITION[0] -= self.bar_movement_speed

  def set_bar_moving_spead(self, level_time):
    # Calculate movement speed based on level time
    total_frames = level_time * 60
    movement_speed = SEGMENT_WIDTH / total_frames
    self.bar_movement_speed = movement_speed
