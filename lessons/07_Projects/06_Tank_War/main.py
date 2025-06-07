import pygame
import random
from pathlib import Path

d = Path(__file__).parent
images_dir = d / "images" if (d / "images").exists() else d / "assets"

pygame.init()
player_count = 0

class Settings():
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 400
    PLAYER_SPEED = 10
    FPS = 30

screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("tank game")

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, player, angle, velocity):
        super().__init__()
        self.proj_ID = player.player_ID
        self.velocity = pygame.Vector2(0, -1).rotate(angle) * velocity
        self.image = pygame.image.load(images_dir/'bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=player.rect.center)

    def update(self):
        self.rect.center += self.velocity


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global player_count, running
        self.images = [
            pygame.image.load(images_dir/'player_blue.png').convert_alpha(),
            pygame.image.load(images_dir/'player_red.png').convert_alpha()
        ]
        self.player_ID = player_count
        player_count += 1

        self.original_image = self.images[self.player_ID]
        self.original_image = pygame.transform.scale(self.original_image, (100, 100))  # consistent scaling
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        self.rect[0] = Settings.SCREEN_WIDTH / 6
        self.rect[1] = Settings.SCREEN_WIDTH / 2
        self.speed = Settings.PLAYER_SPEED
        self.angle = 0
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.velocity = pygame.Vector2(0, 0)
        self.health = 100
        self.damage = 10

    def update(self):
        global players,projectiles,game_over
        spritecollision = pygame.sprite.groupcollide(players, projectiles, dokilla=False, dokillb=False)
        if spritecollision:
            for player in spritecollision:
                for projectile in spritecollision[player]:
                    if self.player_ID == player.player_ID and not self.player_ID == projectile.proj_ID:
                        projectile.kill()
                        player.health -= self.damage
                        print(player.health)
        if self.health <= 0:
            self.kill()
            game_over = True


        

                        
        keys = pygame.key.get_pressed()

        if self.player_ID == 0:
            if keys[pygame.K_a]:
                self.angle -= 5
            if keys[pygame.K_d]:
                self.angle += 5
            if keys[pygame.K_w]:
                self.velocity += pygame.Vector2(0, -0.5).rotate(self.angle)
            if keys[pygame.K_s]:
                self.shoot()
                
        else:
            if keys[pygame.K_LEFT]:
                self.angle -= 5
            if keys[pygame.K_RIGHT]:
                self.angle += 5
            if keys[pygame.K_UP]:
                self.velocity += pygame.Vector2(0, -0.5).rotate(self.angle)
            if keys[pygame.K_DOWN]:
                self.shoot()
                
        self.velocity *= 0.95
        self.rect.center += self.velocity

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        global players
        if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()
            new_projectile = Projectile(self, self.angle, 15)
            new_projectile.proj_ID = self.player_ID
            all_sprites.add(new_projectile)
            projectiles.add(new_projectile)
   
            
test = Player()
test2 = Player()
players = pygame.sprite.Group(test, test2)
projectiles = pygame.sprite.Group()

all_sprites = pygame.sprite.Group(test, test2)


def reset_game():
    global test, test2, players, projectiles, all_sprites
    test = Player()
    test2 = Player()
    players = pygame.sprite.Group(test, test2)
    projectiles = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group(test, test2)






# Sprite groups

# Game loop
clock = pygame.time.Clock()
running = True
game_over = False

while running:

    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if game_over == True:
        clock = pygame.time.Clock()
        running = True
        game_over = False
        reset_game()
    





    all_sprites.update()
    all_sprites.draw(screen)
    
    pygame.display.flip()
    clock.tick(Settings.FPS)

pygame.quit()
