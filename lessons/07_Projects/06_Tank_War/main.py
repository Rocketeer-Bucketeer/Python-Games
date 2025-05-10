import pygame
import random
from pathlib import Path


d = Path(__file__).parent
images_dir = d / "images" if (d / "images").exists() else d / "assets"

pygame.init()

class Settings():
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400
    FPS = 30

#screen setup cool
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("ITS TANKING TIME!!!")


class Player(pygame.sprite.Sprite):
    def __init__(self, player_count):
        self.images = [
            pygame.image.load(images_dir/'player_blue').convert_alpha(),
            pygame.image.load(images_dir/'player_red').convert_alpha()
        ]
        self.player_count = player_count
        










running = True
game_over = False
while running:
    screen.fill((255, 255, 255))
    pygame.display.flip()


