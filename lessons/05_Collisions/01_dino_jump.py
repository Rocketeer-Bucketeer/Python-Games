"""
Dino Jump

Use the arrow keys to move the blue square up and down to avoid the black
obstacles. The game should end when the player collides with an obstacle ...
but it does not. It's a work in progress, and you'll have to finish it. 

"""
import pygame
import random
from pathlib import Path

score = 0
game_over = False
# Initialize Pygame
pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"

# Screen dimensions
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Jump")

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# FPS
FPS = 60

# Player attributes
PLAYER_SIZE = 20

player_speed = 15

# Obstacle attributes
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 20
obstacle_speed = 5

# Font
font = pygame.font.SysFont(None, 36)


# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - OBSTACLE_HEIGHT - 10

        self.explosion = pygame.image.load(images_dir / "explosion1.gif")

    def update(self):
        global score
        self.rect.x -= obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.right < 0:
            self.kill()
            score += 1


    def explode(self): 
        global game_over
        """Replace the image with an explosition image."""
        
        # Load the explosion image
        self.image = self.explosion
        self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.rect = self.image.get_rect(center=self.rect.center)
        game_over = True
        


# Define a player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - PLAYER_SIZE - 10
        self.speed = player_speed
        self.gravity = 0.3
        self.jump_velocity = 6
        self.velocity = 0
        self.is_jumping = False




    def update(self):
        self.rect.y += self.velocity
        self.velocity += self.gravity
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.is_jumping == False:
            self.velocity = -self.jump_velocity
            self.is_jumping = True

        # Keep the player on screen
        if self.rect.top < 0:
            self.rect.top = 0
            print("hi")
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.is_jumping = False


# Create a player object
player = Player()
player_group = pygame.sprite.GroupSingle(player)



# Add obstacles periodically



# Main game loop
class game_loop():
    global score
    global game_over
    clock = pygame.time.Clock()
    
    last_obstacle_time = pygame.time.get_ticks()

    # Group for obstacles
    obstacles = pygame.sprite.Group()

    player = Player()

    obstacle_count = 0


    while not game_over:
        def add_obstacle(obstacles):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.25 means that there is a 25% chance of adding an obstacle. Since
    # add_obstacle() is called every 100ms, this means that on average, an
    # obstacle will be added every 400ms.
    # The combination of the randomness and the time allows for random
    # obstacles, but not too close together. 
     
            if random.random() < 0.35:
                obstacle = Obstacle()
                obstacles.add(obstacle)
                return 0
            return 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Update player
        player.update()

        # Add obstacles and update
        if pygame.time.get_ticks() - last_obstacle_time > 500:
            last_obstacle_time = pygame.time.get_ticks()
            obstacle_count += add_obstacle(obstacles)
        
        obstacles.update()

        # Check for collisions
        collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
        if collider:
            collider[0].explode()
       
        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, player)
        obstacles.draw(screen)

        # Display obstacle count
        obstacle_text = font.render(f"Obstacles: {score}", True, BLACK)
        print(score)
        screen.blit(obstacle_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

    # Game over screen
    print("Game oveR????")
    


if __name__ == "__main__":
    game_loop()
