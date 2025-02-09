import pygame
from Settings import screen, clock, BLACK, font, WHITE, RED, GRAY, WIDTH
from gameLogic import reset_game, score, high_score, wave
from player import player
from enemyLogic import enemies
from items import items
from dungeon import walls

reset_game()
running = True

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot(walls)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()

    keys = pygame.key.get_pressed()
    player.move(keys, walls)
    player.draw(screen)
    player.update_bullets(walls)

    for enemy in enemies:
        enemy.draw(screen)

    for item in items:
        item.draw(screen)

    for wall in walls:
        pygame.draw.rect(screen, GRAY, wall)

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 10))

    wave_text = font.render(f"Wave: {wave}", True, WHITE)
    screen.blit(wave_text, (10, 40))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
