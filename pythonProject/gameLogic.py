import random
import pygame
from Settings import screen, clock
from enemyLogic import Enemy, Boss
from dungeon import generate_dungeon, walls

def reset_game(player):
    """Resets the game state."""
    player.rect.x, player.rect.y = 400, 300
    player.health = 3
    player.has_shield = False
    player.shield_strength = 0
    global enemies, items, wave, score
    enemies = []
    items = []
    wave = 1
    score = 0
    spawn_wave()

def spawn_wave():
    """Spawns a new wave of enemies."""
    global enemies, wave
    enemies = [Enemy(random.randint(100, 700), random.randint(100, 500), random.choice(["melee", "ranged", "exploding"])) for _ in range(wave * 3)]
    if wave % 5 == 0:
        enemies.append(Boss(random.randint(100, 700), random.randint(100, 500)))

def game_loop(player):
    """Main game loop."""
    running = True
    while running:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot(player.bullets)

        player.move(pygame.key.get_pressed(), walls)
        player.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)
