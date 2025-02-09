import pygame
from Settings import GREEN

class Player:
    """Represents the player character."""

    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 5
        self.health = 3
        self.has_shield = False
        self.shield_strength = 0
        self.bullets = []

    def move(self, keys, walls):
        """Handles player movement, preventing wall collisions."""
        new_x, new_y = self.rect.x, self.rect.y

        if keys[pygame.K_w]: new_y -= self.speed
        if keys[pygame.K_s]: new_y += self.speed
        if keys[pygame.K_a]: new_x -= self.speed
        if keys[pygame.K_d]: new_x += self.speed

        new_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)

        if not any(new_rect.colliderect(wall) for wall in walls):
            self.rect.x, self.rect.y = new_x, new_y

    def shoot(self, bullets):
        """Shoots a bullet upwards."""
        bullet = pygame.Rect(self.rect.centerx, self.rect.top, 10, 10)
        bullets.append(bullet)

    def draw(self, screen):
        """Draws the player."""
        pygame.draw.rect(screen, GREEN, self.rect)
