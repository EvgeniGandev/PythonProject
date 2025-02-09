import pygame
from Settings import RED, BLUE

class Item:
    """Represents collectible items (health, shield)."""

    def __init__(self, item_type, x, y):
        self.item_type = item_type
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = RED if item_type == "health" else BLUE if item_type == "shield" else None

    def draw(self, screen):
        """Draws the item."""
        if self.color:
            pygame.draw.rect(screen, self.color, self.rect)
