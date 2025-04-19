import pygame
import random
from pathlib import Path

d = Path(__file__).parent # The directory that holds the script
images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"
# Initialize Pygame 
pygame.init()

class Settings:
    """A class to store all settings for the game."""
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400
    BACKGROUND_SCROLL_SPEED = 10
    FPS = 30
    GRAVITY = 2
    SPEED = 20
    JUMP_VELOCITY = 20
    PIPE_WIDTH = 50
    PIPE_HEIGHT = 130
    REAL_SPEED = 20   
    PIPE_GAP = 100

# Initialize screen
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("flappy bird game!!!")

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

        self.images = [pygame.image.load(images_dir/'bluebird-downflap.png').convert_alpha(),
                       pygame.image.load(images_dir/'bluebird-midflap.png').convert_alpha(),
                       pygame.image.load(images_dir/'bluebird-upflap.png').convert_alpha()]

        self.speed = Settings.SPEED

        self.current_image_counter = 0 # current image number for list probably 
  
        self.image = self.images[0] # placeholder.     


        self.rect = self.image.get_rect()
        self.rect[0] = Settings.SCREEN_WIDTH / 6 # x  or like forward posiotion i think
        self.rect[1] = Settings.SCREEN_HEIGHT / 2 # y hegiht

    def update(self):
        self.current_image_counter = (self.current_image_counter + 1) % 3 # update current image index
        self.image = self.images[self.current_image_counter] # set image to the current image counter variable
        self.speed += Settings.GRAVITY 
        self.rect[1] += self.speed # updt height
    
    def jump(self):
        self.speed = -Settings.JUMP_VELOCITY

 
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, backwards):
        super().__init__()
        self.original_image = pygame.image.load(images_dir/'pipe-green.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (Settings.PIPE_WIDTH, Settings.PIPE_HEIGHT))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.backwards = backwards
        self.reset(x, y, backwards)

    def reset(self, x, y, backwards):
        self.image = pygame.transform.flip(self.original_image, False, True) if backwards else self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        if backwards:
            Settings.PIPE_HEIGHT = self.rect.height - y  # flip pipe
        else:
            Settings.PIPE_HEIGHT = Settings.SCREEN_HEIGHT - y

    def update(self):
        self.rect.x -= Settings.REAL_SPEED
        if self.rect.right < 0:
            Settings.PIPE_HEIGHT = random.randint(0, 200)
            self.reset(Settings.SCREEN_WIDTH, Settings.PIPE_HEIGHT if not self.backwards else Settings.SCREEN_HEIGHT - Settings.PIPE_HEIGHT - Settings.PIPE_GAP, self.backwards)



def getPipePos(x):
    size = random.randint(0, 200)
    top_pipe = Pipe(x, size, True)
    bottom_pipe = Pipe(x, (200 - size) + Settings.PIPE_GAP, False)
    return bottom_pipe, top_pipe
    

def main(): 
    """Run the main game loop."""
    running = True

  
    flappy_group = pygame.sprite.Group()
    flappy = Player() 
    flappy_group.add(flappy)

    pipe_group = pygame.sprite.Group()
    for i in range(1):
        pipes = getPipePos(Settings.SCREEN_WIDTH + 800)
        pipe_group.add(pipes[1])
        pipe_group.add(pipes[0])
        print(pipe_group)




    bg = Background()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bg)

    clock = pygame.time.Clock()
    print(pipe_group)

    while running:   
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_SPACE:
                    flappy.jump()
                    ("hi")

 
        all_sprites.update()
        all_sprites.draw(screen)
        flappy.update()
        pipe_group.update()
        
        
        flappy_group.draw(screen)
        pipe_group.draw(screen)
         
        pygame.display.flip()
        
        clock.tick(Settings.FPS)

    pygame.quit()





if __name__ == "__main__":
    main()
