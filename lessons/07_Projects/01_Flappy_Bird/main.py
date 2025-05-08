import pygame
import random
from pathlib import Path

# Setup paths
d = Path(__file__).parent
images_dir = d / "images" if (d / "images").exists() else d / "assets"

pygame.init()

class Settings:
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400
    BACKGROUND_SCROLL_SPEED = 4
    FPS = 60
    GRAVITY = 0.75
    SPEED = 0
    JUMP_VELOCITY = 10
    PIPE_WIDTH = 50
    PIPE_HEIGHT = 130
    REAL_SPEED = 5
    PIPE_GAP = 200

# Setup screen
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("flappy bird game!!!")

# Background
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((Settings.SCREEN_WIDTH * 2, Settings.SCREEN_HEIGHT))
        bg = pygame.image.load(images_dir / 'background.png').convert()
        bg = pygame.transform.scale(bg, (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
        self.image.blit(bg, (0, 0))
        self.image.blit(bg, (Settings.SCREEN_WIDTH, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 0

    def update(self):
        self.rect.x -= Settings.BACKGROUND_SCROLL_SPEED
        if self.rect.right <= Settings.SCREEN_WIDTH:
            self.rect.x = 0

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = [
            pygame.image.load(images_dir/'bluebird-downflap.png').convert_alpha(),
            pygame.image.load(images_dir/'bluebird-midflap.png').convert_alpha(),
            pygame.image.load(images_dir/'bluebird-upflap.png').convert_alpha()
        ]
        self.current_image_counter = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect[0] = Settings.SCREEN_WIDTH / 6
        self.rect[1] = Settings.SCREEN_HEIGHT / 2
        self.speed = Settings.SPEED

    def update(self):
        self.current_image_counter = (self.current_image_counter + 1) % len(self.images)
        self.image = self.images[self.current_image_counter]
        self.speed += Settings.GRAVITY
        self.rect[1] += self.speed

    def jump(self):
        self.speed = -Settings.JUMP_VELOCITY

# Pipe
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, backwards):
        super().__init__()
        self.original_image = pygame.image.load(images_dir/'pipe-green.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (Settings.PIPE_WIDTH, Settings.PIPE_HEIGHT))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.backwards = backwards
        self.reset(x, y, backwards)

    def reset(self, x, y, backwards):
        self.image = pygame.transform.flip(self.original_image, False, True) if backwards else self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.scored = False

    def update(self):
        self.rect.x -= Settings.REAL_SPEED
        if self.rect.right < 0:
            size = random.randint(50, Settings.SCREEN_HEIGHT - Settings.PIPE_GAP - 50)
            new_y = size if self.backwards else size + Settings.PIPE_GAP
            self.reset(Settings.SCREEN_WIDTH + 200, new_y if not self.backwards else size - Settings.PIPE_HEIGHT, self.backwards)

def getPipePos(x):
    size = random.randint(50, Settings.SCREEN_HEIGHT - Settings.PIPE_GAP - 50)
    top_pipe = Pipe(x, size - Settings.PIPE_HEIGHT, True)
    bottom_pipe = Pipe(x, size + Settings.PIPE_GAP, False)
    return bottom_pipe, top_pipe
def main():
    def reset_game():
        nonlocal flappy, flappy_group, pipe_group, score, game_over
        flappy = Player()
        flappy.rect.y -= 40  
        flappy.speed = -Settings.JUMP_VELOCITY / 1.5  

        flappy_group = pygame.sprite.Group(flappy)

        pipe_group = pygame.sprite.Group()
        pipes = getPipePos(Settings.SCREEN_WIDTH + 200)
        pipe_group.add(pipes)

        score = 0
        game_over = False


    running = True
    game_over = False
    score = 0
    font = pygame.font.SysFont(None, 32)

    flappy = Player()
    flappy_group = pygame.sprite.Group(flappy)

    pipe_group = pygame.sprite.Group()
    pipes = getPipePos(Settings.SCREEN_WIDTH + 200)
    pipe_group.add(pipes)

    bg = Background()
    all_sprites = pygame.sprite.Group(bg)

    clock = pygame.time.Clock()

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                flappy.jump()
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()

        if not game_over:
            all_sprites.update()
            flappy.update()
            pipe_group.update()

            if pygame.sprite.spritecollide(flappy, pipe_group, False):
                game_over = True
            if flappy.rect.top < 0 or flappy.rect.bottom > Settings.SCREEN_HEIGHT:
                game_over = True

            for pipe in pipe_group:
                if pipe.rect.right < flappy.rect.left and not getattr(pipe, "scored", False):
                    score += 0.5
                    pipe.scored = True

       
        all_sprites.draw(screen)
        pipe_group.draw(screen)
        flappy_group.draw(screen)

        score_txt = font.render(f"Score: {int(score)}", True, (255, 255, 255))
        screen.blit(score_txt, (20, 20))

        if game_over:
            text_thing = font.render("Game Over - Press SPACE to restart", True, (255, 0, 0))
            screen.blit(text_thing, (Settings.SCREEN_WIDTH//2 - text_thing.get_width()//2, Settings.SCREEN_HEIGHT//2))

        pygame.display.flip()
        clock.tick(Settings.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
