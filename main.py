import pygame
from enemy_manager import EnemyManager
from level_manager import LevelManager
from tower_manager import TowerManager
from grid import Grid
from hud import Hud
from config import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_HEIGHT, GRID_WIDTH, GRID_HEIGHT, LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT, LOADING_BAR_COLOR, LOADING_BAR_BG_COLOR, LOADING_BAR_POSITION

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Defense")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
menu_font = pygame.font.Font(None, 74)  # Font for the main menu title

grid = Grid(screen)
hud = Hud(screen)
enemy_manager = EnemyManager(screen, hud)
tower_manager = TowerManager(screen)
level_manager = LevelManager()

# Define a custom event for updating coins
UPDATE_COINS_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(UPDATE_COINS_EVENT, 1000)  # 1000 milliseconds = 1 second

title_text = menu_font.render("Python Tower Defence", True, (255, 255, 255))
title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
start_button_text = menu_font.render("Start", True, (255, 255, 255))
start_button_rect = start_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

game_over_text = menu_font.render("Game Over", True, (255, 255, 255))
game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
restart_button_text = menu_font.render("Restart", True, (255, 255, 255))
restart_button_rect = restart_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

def update():
  grid.update()
  enemy_manager.update()
  tower_manager.update(enemy_manager.enemies)
  # level_manager.update()
  hud.update()

def draw():
  screen.fill((100, 100, 100))

def draw_loading_bar(screen, progress):
  # Draw the background of the loading bar
  pygame.draw.rect(screen, LOADING_BAR_BG_COLOR, (*LOADING_BAR_POSITION, LOADING_BAR_WIDTH, LOADING_BAR_HEIGHT))
  
  # Calculate the width of the filled part of the loading bar
  filled_width = int(LOADING_BAR_WIDTH * progress)
  
  # Draw the filled part of the loading bar
  pygame.draw.rect(screen, LOADING_BAR_COLOR, (*LOADING_BAR_POSITION, filled_width, LOADING_BAR_HEIGHT))
  coins_text = font.render(f"Loading: Level 1", True, (255, 255, 255))
  coins_text_rect = coins_text.get_rect(center=(LOADING_BAR_POSITION[0] + LOADING_BAR_WIDTH // 2, LOADING_BAR_POSITION[1] - 20))
  screen.blit(coins_text, coins_text_rect)

def draw_main_menu(screen):
  screen.fill((100, 100, 100))

  # Draw the title
  screen.blit(title_text, title_rect)

  # Draw the start button
  pygame.draw.rect(screen, (0, 200, 0), start_button_rect.inflate(20, 10))  # Draw button background
  screen.blit(start_button_text, start_button_rect)

def draw_game_over(screen):
  screen.blit(game_over_text, game_over_rect)

  # Draw the start button
  pygame.draw.rect(screen, (0, 200, 0), restart_button_rect.inflate(20, 10))  # Draw button background
  screen.blit(restart_button_text, restart_button_rect)

# Game loop
def main():
  running = True
  level_loading = 0
  level_loaded = False
  show_main_menu = True
  show_game_over_screen = False

  level_manager.create([1,2,3,4])
  enemy_manager.rows = grid.rows

  while running:
    clock.tick(60) 
    # Event handling
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if event.type == pygame.MOUSEBUTTONDOWN:
        if show_main_menu:
          if start_button_rect.collidepoint(event.pos):
            show_main_menu = False
        elif show_game_over_screen:
          if restart_button_rect.collidepoint(event.pos):
            show_game_over_screen = False
            show_main_menu = True
            hud.reset()
        else:
          if event.pos[1] >= SCREEN_HEIGHT - 200:
            hud.handle_click(event.pos)
          else:
            grid_pos, grid_square = grid.get_square_pos(event.pos)
            if grid_pos and hud.selected_card and hud.buy_tower(hud.selected_card.cost):
              hud.update_coins(-hud.selected_card.cost)
              tower_manager.create(grid_pos, hud.selected_card)
              grid.update_square(grid_square, 1)
              enemy_manager.recalaulate_path()
      if event.type == UPDATE_COINS_EVENT:
        hud.update_coins(1)

    # Keyboard input handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
      running = False

    if show_main_menu:
      draw_main_menu(screen)
    elif show_game_over_screen:
      draw_game_over(screen)
    
    else:
      draw()
      update()

      if hud.game_over:
        show_game_over_screen = True

      if level_loading < 240:
        level_loading +=1
        progress = level_loading / 240
        draw_loading_bar(screen, progress)
      elif level_loaded == False:
        enemy_manager.update_enemy_spawner(level_manager.levels[0].spawn_points, level_manager.levels[0].enemy_types, level_manager.levels[0].spawn_speed)
        level_loaded = True

      if level_loaded and len(enemy_manager.enemies) == 0:
        print(len(enemy_manager.enemies) )
        print(len(enemy_manager.enemies) == 0 )
        print('level done')
  
    # Update the display
    pygame.display.flip()
  # Quit the game
  pygame.quit()

if __name__ == "__main__":
  main()
