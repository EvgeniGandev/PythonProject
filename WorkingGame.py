import random
import math
import pygame
from typing import List, Dict, Optional

#Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (30, 30, 30)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)

# Enemy bullets list
enemy_bullets: List[Dict[str, float]] = []

# Dungeon walls
walls: List[pygame.Rect] = []

# Score and waves
score: int = 0
high_score: int = 0
wave: int = 1
remaining_enemies: int = 0

# Player items
HEALING_ITEM_CHANCE: float = 0.3  # 30% chance to drop
SHIELD_ITEM_CHANCE: float = 0.2    # 20% chance to drop

# Player state
player_health: int = 3
has_shield: bool = False
shield_strength: int = 0  # Amount of damage the shield can absorb


class Item:
    """Class representing an item in the game."""
    
    def __init__(self, item_type: str, x: int, y: int) -> None:
        self.item_type: str = item_type
        self.rect: pygame.Rect = pygame.Rect(x, y, 20, 20)  # Smaller rectangles
        self.color: Optional[tuple[int, int, int]] = self.get_color(item_type)

    def get_color(self, item_type: str) -> Optional[tuple[int, int, int]]:
        """Get the color of the item based on its type."""
        if item_type == 'health':
            return RED  # Red
        elif item_type == 'shield':
            return BLUE  # Blue
        return None


items: List[Item] = []


def spawn_item(item_type: str, x: int, y: int) -> None:
    """Spawn an item at the specified location."""
    new_item = Item(item_type, x, y)
    items.append(new_item)


def spawn_wave() -> None:
    """Spawn a new wave of enemies."""
    global remaining_enemies
    remaining_enemies = wave * 3
    for _ in range(remaining_enemies):
        enemy_type = random.choice(["melee", "ranged", "exploding"])
        enemies.append(Enemy(random.randint(100, 700), random.randint(100, 500), enemy_type))
    
    # Spawn a boss every 5th wave
    if wave % 5 == 0:
        enemies.append(Boss(random.randint(100, 700), random.randint(100, 500)))


class Room:
    """Class representing a room in the dungeon."""
    
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, w, h)
        walls.append(self.rect)


def generate_dungeon() -> None:
    """Generate random dungeon walls."""
    for _ in range(6):  # Generate 6 random walls
        x, y, w, h = random.randint(50, 600), random.randint(50, 400), 150, 20
        walls.append(pygame.Rect(x, y, w, h))


generate_dungeon()


def get_valid_spawn() -> pygame.Rect:
    """Get a valid spawn location for the player."""
    while True:
        spawn_x, spawn_y = random.randint(50, 750), random.randint(50, 550)
        player_rect = pygame.Rect(spawn_x, spawn_y, 40, 40)
        if not any(player_rect.colliderect(wall) for wall in walls):
            return player_rect


def reset_game() -> None:
    """Reset the game state."""
    global player, player_bullets, enemies, score, wave, remaining_enemies, has_shield, shield_strength, items, player_health
    player = get_valid_spawn()
    player_health = 3  # Reset the global player_health variable
    player_bullets = []
    enemies.clear()
    score = 0
    wave = 1
    has_shield = False
    shield_strength = 0  # Reset shield strength
    items.clear()  # Clear items for a new game
    spawn_wave()


player: pygame.Rect = get_valid_spawn()
player_speed: int = 5
player_bullets: List[pygame.Rect] = []
enemies: List['Enemy'] = []


class Enemy:
    """Class representing an enemy in the game."""
    
    def __init__(self, x: int, y: int, enemy_type: str, health: int = 1) -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, 40, 40)
        self.speed: int = 2
        self.enemy_type: str = enemy_type
        self.health: int = health
        self.exploded: bool = False
        self.shoot_cooldown: int = 50  # Controls how often ranged enemies shoot
        self.melee_attack_cooldown: int = 100  # Cooldown for melee attack

    def move_towards_player(self) -> None:
        """Move the enemy towards the player."""
        dx, dy = player.x - self.rect.x, player.y - self.rect.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            new_x = self.rect.x + (dx / distance) * self.speed
            new_y = self.rect.y + (dy / distance) * self.speed
            new_rect = pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)
            if not any(new_rect.colliderect(wall) for wall in walls):
                self.rect.x = new_x
                self.rect.y = new_y

    def attack(self) -> None:
        """Perform an attack on the player."""
        global player_health
        if self.enemy_type == "exploding" and not self.exploded:
            if self.rect.colliderect(player):
                if not has_shield:
                    player_health -= 1
                self.exploded = True
        elif self.enemy_type == "ranged":
            self.shoot_cooldown -= 1
            if self.shoot_cooldown <= 0:  # Shoot after cooldown resets
                dx, dy = player.centerx - self.rect.centerx, player.centery - self.rect.centery
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance != 0:
                    bullet = {
                        "rect": pygame.Rect(self.rect.centerx, self.rect.centery, 10, 10),
                        "vx": (dx / distance) * 4,  # Adjust bullet speed
                        "vy": (dy / distance) * 4
                    }
                    enemy_bullets.append(bullet)
                self.shoot_cooldown = 50  # Reset cooldown
        elif self.enemy_type == "melee":
            if self.rect.colliderect(player) and self.melee_attack_cooldown <= 0:
                if not has_shield:
                    player_health -= 1  # Damage player if colliding
                self.melee_attack_cooldown = 100  # Reset melee attack cooldown

    def update(self) -> None:
        """Updates enemy behavior each frame."""
        self.move_towards_player()
        self.attack()
        if self.melee_attack_cooldown > 0:
            self.melee_attack_cooldown -= 1  # Decrease cooldown

    def drop_item(self) -> Optional[str]:
        """Randomly drops an item when defeated."""
        drop_chance = random.random()
        if drop_chance < HEALING_ITEM_CHANCE:
            return "health"
        elif drop_chance < HEALING_ITEM_CHANCE + SHIELD_ITEM_CHANCE:
            return "shield"
        return None


class Boss(Enemy):
    """Class representing a boss enemy."""
    
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, "boss", health=5)
        self.sonic_attack_cooldown: int = 100  # Cooldown for sonic attack

    def sonic_attack(self) -> None:
        """Perform a sonic attack that damages the player."""
        if self.sonic_attack_cooldown <= 0:
            if self.rect.colliderect(player):
                if not has_shield:
                    player_health -= 2  # Boss does more damage
            self.sonic_attack_cooldown = 200  # Reset cooldown
        else:
            self.sonic_attack_cooldown -= 1

    def update(self) -> None:
        """Update the boss's behavior."""
        super().update()
        self.sonic_attack()


def pick_up_shield() -> None:
    """Pick up a shield item."""
    global has_shield, shield_strength
    has_shield = True
    shield_strength = 1  # Set the shield strength (can be adjusted)


# Game loop
running: bool = True
spawn_wave()
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player.centerx, player.centery, 10, 10)
                if not any(bullet.colliderect(wall) for wall in walls):
                    player_bullets.append(bullet)
            if event.key == pygame.K_r:  # Allow reset at any time
                reset_game()

    if player_health <= 0:
        if score > high_score:
            high_score = score
        game_over_text = font.render("Game Over! Press 'R' to Restart", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()
        continue

    # Player movement (with screen boundary check)
    keys = pygame.key.get_pressed()
    new_x, new_y = player.x, player.y
    if keys[pygame.K_w] and player.top > 0: 
        new_y -= player_speed
    if keys[pygame.K_s] and player.bottom < HEIGHT: 
        new_y += player_speed
    if keys[pygame.K_a] and player.left > 0: 
        new_x -= player_speed
    if keys[pygame.K_d] and player.right < WIDTH: 
        new_x += player_speed

    # Check if movement collides with walls
    new_rect = pygame.Rect(new_x, new_y, player.width, player.height)
    if not any(new_rect.colliderect(wall) for wall in walls):
        player.x, player.y = new_x, new_y

    for wall in walls:
        pygame.draw.rect(screen, GRAY, wall)

    pygame.draw.rect(screen, GREEN, player)

    # Update player bullets
    player_bullets = [bullet for bullet in player_bullets if bullet.y > 0 and not any(bullet.colliderect(wall) for wall in walls)]
    for bullet in player_bullets:
        bullet.y -= 5
        pygame.draw.rect(screen, WHITE, bullet)

    for enemy in enemies[:]:
        enemy.update()
        color = ORANGE if enemy.enemy_type == "boss" else (RED if enemy.enemy_type == "melee" else BLUE)
        pygame.draw.rect(screen, color, enemy.rect)
        for bullet in player_bullets[:]:
            if bullet.colliderect(enemy.rect):
                item_dropped = enemy.drop_item()
                if item_dropped == "health":
                    if player_health < 3:
                        player_health += 1
                elif item_dropped == "shield":
                    pick_up_shield()  # Call the function to pick up a shield

                if enemy in enemies:  # Check if enemy is still in the list
                    enemies.remove(enemy)
                if bullet in player_bullets:  # Check if bullet is still in the list
                    player_bullets.remove(bullet)
                score += 100
                remaining_enemies -= 1

                # Spawn the item at the enemy's position
                spawn_item(item_dropped, enemy.rect.x, enemy.rect.y)

    if remaining_enemies == 0:
        wave += 1
        spawn_wave()
    
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH - 250, 40))
    # Display player health
    health_text = font.render(f"Health: {player_health}", True, WHITE)
    screen.blit(health_text, (10, 10))
    # Display current wave
    wave_text = font.render(f"Wave: {wave}", True, WHITE)
    screen.blit(wave_text, (10, 40))

    # Move and draw enemy bullets
    for bullet in enemy_bullets[:]:
        bullet["rect"].x += bullet["vx"]
        bullet["rect"].y += bullet["vy"]
        
        # Check if the bullet rectangle is valid before drawing
        if bullet["rect"].y > 0 and bullet["rect"].y < HEIGHT:
            pygame.draw.rect(screen, ORANGE, bullet["rect"])
            if bullet["rect"].colliderect(player):
                if has_shield:
                    shield_strength -= 1  # Reduce shield strength
                    if shield_strength <= 0:
                        has_shield = False  # Remove shield if it breaks
                else:
                    player_health -= 1  # Damage player if no shield
                enemy_bullets.remove(bullet)

    # Draw items and check for collection
    for item in items[:]:
        if item.color:  # Check if color is valid
            pygame.draw.rect(screen, item.color, item.rect)
            if item.rect.colliderect(player):  # Check for item collection
                if item.item_type == "health" and player_health < 3:
                    player_health += 1
                elif item.item_type == "shield":
                    pick_up_shield()  # Call the function to pick up a shield
                items.remove(item)  # Remove item after collection

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
