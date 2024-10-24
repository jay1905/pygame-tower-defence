import pygame
from config import CELL_SIZE

class TowerCard:
	def __init__(self, position, color_base, color_top, cost):
		self.position = position
		self.color_base = color_base
		self.color_top = color_top
		self.range = 60
		self.cost = cost
		self.font = pygame.font.Font(None, 36)
		self.width = 60
		self.height = 80
		self.border_color = (255, 255, 255)
		self.card_color = (50, 50, 50)
		self.border_radius = 10
		self.selected = False

	def draw_rounded_rect(self, screen, rect, color, radius):
		pygame.draw.rect(screen, color, rect, border_radius=radius)

	def draw(self, screen):
		card_x, card_y = self.position
		tower_width = CELL_SIZE
		tower_height = CELL_SIZE

		# Draw the card background with rounded corners
		card_rect = pygame.Rect(card_x, card_y, self.width, self.height)
		self.draw_rounded_rect(screen, card_rect, self.border_color, self.border_radius)

		# Draw the inner card background
		inner_rect = pygame.Rect(card_x + 5, card_y + 5, self.width - 10, self.height - 10)
		self.draw_rounded_rect(screen, inner_rect, self.card_color, self.border_radius)

		# Calculate positions inside the card
		tower_x = card_x + 20
		tower_y = card_y + 20

		# Draw the tower base (rectangle)
		pygame.draw.rect(screen, self.color_base, (tower_x, tower_y, tower_width, tower_height))

		# Draw the tower top (circle)
		pygame.draw.circle(screen, self.color_top, (tower_x + tower_width // 2, tower_y), tower_width // 2)

		# Draw the tower cost under the tower representation
		cost_text = self.font.render(f"{self.cost}", True, (255, 255, 255))
		text_rect = cost_text.get_rect(center=(tower_x + tower_width // 2, tower_y + tower_height + 20))
		screen.blit(cost_text, text_rect)
		# draw red border if selected
		if self.selected:
			pygame.draw.rect(screen, (255, 100, 100), card_rect, 3, self.border_radius)
