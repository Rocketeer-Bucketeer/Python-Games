import pygame
import random
from pathlib import Path

d = Path(__file__).parent # The directory that holds the script
images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"
# Initialize Pygame
pygame.init()

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BACKGROUND_SCROLL_SPEED = 10
    FPS = 30

# Initialize screen
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("Background Scroll")

# Define background class
class Background(pygame.sprite.Sprite):
    """Represents the scrolling background in the game."""
    def __init__(self):
        super().__init__()
        
        # The Sprite image is 2x as wide as the screen
        self.image = pygame.Surface((Settings.SCREEN_WIDTH * 2, Settings.SCREEN_HEIGHT))
        
        # Load the background image and scale it to the screen size. Note the convert() call. 
        # This converts the form of the image to be more efficient. 
        orig_image= pygame.image.load(images_dir/'background.png').convert()
        orig_image = pygame.transform.scale(orig_image, (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        
        # Then, copy it into the self.image surface twice
        self.image.blit(orig_image, (0, 0))
        self.image.blit(orig_image, (Settings.SCREEN_WIDTH, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self):
        """Update the position of the background."""
        
        self.rect.x -= Settings.BACKGROUND_SCROLL_SPEED
        
        if self.rect.right <= Settings.SCREEN_WIDTH:
            self.rect.x = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load(d/'bluebird-downflap.png').convert_alpha(),
                       pygame.image.load(d/'bluebird-midflap.png').convert_alpha(),
                       pygame.image.load(d/'bluebird-upflap.png').convert_alpha()]

        self.speed = 20

        self.current_image_counter = 0 # current image number for list probably 

        self.image = pygame.image.load(d/'bluebird-downflap.png').convert_alpha() # placeholder


        self.rect = self.image.get_rect()
        self.rect[0] = Settings.SCREEN_WIDHT / 6 # x
        self.rect[1] = Settings.SCREEN_HEIGHT / 2 # y

    def update(self):
        pass
    

    
        


        






def main():
    """Run the main game loop."""
    running = True


    bg = Background()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bg)

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        
        clock.tick(Settings.FPS)

    pygame.quit()





if __name__ == "__main__":
    main()
