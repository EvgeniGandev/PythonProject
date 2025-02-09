import pygame
import random
import math
from Settings import RED, BLUE, ORANGE, HEALING_ITEM_CHANCE, SHIELD_ITEM_CHANCE

class Enemy:
    """Represents an enemy."""
    
    def __init__(self, x: int, y: int, enemy_type: str):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 2
        self.enemy_type = enemy_type
        self.health = 1
        self.exploded = False
        self.shoot_cooldown = 50
        self.melee_attack_cooldown = 100

    def move_towards(self, player, walls):
        """Moves towards the player while avoiding walls."""
        dx, dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            new_x = self.rect.x + (dx / distance) * self.speed
            new_y = self.rect.y + (dy / distance) * self.speed
            new_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)

            if not any(new_rect.colliderect(wall) for wall in walls):
                self.rect.x, self.rect.y = new_x, new_y

    def attack(self, player):
        """Handles attacks based on enemy type."""
        if self.enemy_type == "melee" and self.rect.colliderect(player.rect):
            if not player.has_shield:
                player.health -= 1

    def draw(self, screen):
        """Draws the enemy."""
        color = ORANGE if self.enemy_type == "boss" else (RED if self.enemy_type == "melee" else BLUE)
        pygame.draw.rect(screen, color, self.rect)

class Boss(Enemy):
    """Boss enemy with extra attacks."""
    
    def __init__(self, x, y):
        super().__init__(x, y, "boss")
        self.health = 5
        self.sonic_attack_cooldown = 100

    def sonic_attack(self, player):
        """Special boss attack."""
        if self.sonic_attack_cooldown <= 0 and self.rect.colliderect(player.rect):
            if not player.has_shield:
                player.health -= 2
            self.sonic_attack_cooldown = 200
        else:
            self.sonic_attack_cooldown -= 1
