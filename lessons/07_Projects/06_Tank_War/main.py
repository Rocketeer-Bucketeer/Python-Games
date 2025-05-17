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

#screen setup cool
screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("tank game")



class Projectile(pygame.sprite.Sprite):
    def __init__(self, position, angle, velocity):
        super().__init__()

        self.velocity = pygame.Vector2(0, -1).rotate(angle) * velocity

        self.images = [
            pygame.image.load(images_dir/'bullet.png').convert_alpha()
        ]

        self.image = self.images[0]
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.center += self.velocity







class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global player_count

        self.images = [
            pygame.image.load(images_dir/'player_blue.png').convert_alpha(),
            pygame.image.load(images_dir/'player_red.png').convert_alpha()
        ]
        self.player_ID = player_count
        player_count += 1
        self.image = self.images[self.player_ID]
        self.rect = self.image.get_rect()
        self.rect[0] = Settings.SCREEN_WIDTH / 6
        self.rect[1] = Settings.SCREEN_WIDTH / 2
        self.speed = Settings.PLAYER_SPEED
        self.angle = 0
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.velocity = pygame.Vector2(0,0)
    
    def update(self):
        keys = pygame.key.get_pressed()
        

        if self.player_ID == 0:
            print("player one controls")
            if keys[pygame.K_a]:
                self.angle -= 5
                print("hihihihi")
            if keys[pygame.K_d]:
                self.angle += 5
            if keys[pygame.K_w]:
                vectorforward = pygame.Vector2(0, -0.1).rotate(self.angle)
                self.velocity += vectorforward
            if keys[pygame.K_s]:
                self.shoot()      
        else:
            print("player two controls")
            if keys[pygame.K_LEFT]:
                self.angle -= 5
            if keys [pygame.K_RIGHT]:
                self.angle += 5
            if keys[pygame.K_UP]:
                vectorforward2 = pygame.Vector2(0, -0.1).rotate(self.angle)
                self.velocity += vectorforward2
            if keys[pygame.K_DOWN]:
                self.shoot()

        self.image = pygame.transform.rotate(self.image, -self.angle)
        self.rec = self.image.get_rect(center=self.rect.center)
        self.rect.center += self.velocity

        super().update()

        # testing
        print(self.player_ID)


    
    def shoot(self):

        if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()
            
            new_projectile = Projectile()



test = Player()
test2 = Player()





        


running = True
game_over = False
while running:
    screen.fill((255, 255, 255))



    pygame.display.flip()


