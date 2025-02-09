import pygame
import random
from Settings import GRAY

walls = []

def generate_dungeon():
    """Generates dungeon walls."""
    global walls
    walls = [pygame.Rect(random.randint(50, 600), random.randint(50, 400), 150, 20) for _ in range(6)]
