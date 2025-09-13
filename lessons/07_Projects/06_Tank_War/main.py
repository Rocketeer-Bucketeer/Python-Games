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
    FPS = 55

screen = pygame.display.set_mode((Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT))
pygame.display.set_caption("tank game")




# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, player, angle, velocity):
        super().__init__()
        self.proj_ID = player.player_ID
        self.damage = player.damage
        self.velocity = pygame.Vector2(0, -1).rotate(angle) * velocity
        self.image = pygame.image.load(images_dir / 'bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=player.rect.center)

    def update(self):
        self.rect.center += self.velocity


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global player_count
        self.images = [
            pygame.image.load(images_dir / 'player_blue.png').convert_alpha(),
            pygame.image.load(images_dir / 'player_red.png').convert_alpha(),
            pygame.image.load(images_dir / 'player_red.png').convert_alpha(),
            pygame.image.load(images_dir / 'player_red.png').convert_alpha(),
            pygame.image.load(images_dir / 'player_red.png').convert_alpha(),
            pygame.image.load(images_dir / 'player_red.png').convert_alpha()
        ]
        self.player_ID = player_count
        player_count += 1

        self.original_image = self.images[self.player_ID]
        self.original_image = pygame.transform.scale(self.original_image, (100, 100))
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.rect[0] = Settings.SCREEN_WIDTH / 6 * (1 if self.player_ID == 0 else 4)
        self.rect[1] = Settings.SCREEN_HEIGHT / 2
        self.speed = Settings.PLAYER_SPEED
        self.angle = 0
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.velocity = pygame.Vector2(0, 0)
        self.health = 100
        self.damage = 5

    def update(self):
        global players, projectiles, game_over, powerups, fpowerups

        spritecollision = pygame.sprite.groupcollide(players, projectiles, False, False)
    
        for player in spritecollision:
            for projectile in spritecollision[player]:
                if player.player_ID != projectile.proj_ID:
                    player.health -= projectile.damage
                    projectile.kill()
                    print(f"Player {player.player_ID} health: {player.health}")

        if self.health <= 0:
            self.kill()
            game_over = True
        
        healcollision = pygame.sprite.groupcollide(players, powerups, False, True)


        for player in healcollision:
            if player.player_ID == 1:
                player.health = player.health + 15
            else:
                player.health = player.health + 15
        

        fpowerupcollision = pygame.sprite.groupcollide(players, fpowerups, False, True)

        for player in fpowerupcollision:
            if player.player_ID == 1:
                player.health = player.health - 15
            else:
                player.health = player.health - 15

        



        keys = pygame.key.get_pressed()
        if self.player_ID == 0:
            if keys[pygame.K_a]:
                self.angle -= 5
            if keys[pygame.K_d]:
                self.angle += 5
            if keys[pygame.K_w]:
                self.velocity += pygame.Vector2(0, -0.35).rotate(self.angle)
            if keys[pygame.K_s]:
                self.shoot()
        else:
            if keys[pygame.K_LEFT]:
                self.angle -= 5
            if keys[pygame.K_RIGHT]:
                self.angle += 5
            if keys[pygame.K_UP]:
                self.velocity += pygame.Vector2(0, -0.35).rotate(self.angle)
            if keys[pygame.K_DOWN]:
                self.shoot()

        self.velocity *= 0.95
        self.rect.center += self.velocity

        self.rect.clamp_ip(screen.get_rect())

        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        if pygame.time.get_ticks() - self.last_shot > self.shoot_delay:
            self.last_shot = pygame.time.get_ticks()
            new_projectile = Projectile(self, self.angle, 15)
            all_sprites.add(new_projectile)
            projectiles.add(new_projectile)


class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(images_dir / 'health_pack.png').convert_alpha()
        self.heal_amount = 15
        self.rect = self.image.get_rect()
        self.rect[0] = random.randint(100, 500)
        self.rect[1] = random.randint(100, 400)

    def heal(self, playerhealed):
        playerhealed.health = playerhealed.health + self.heal_amount
        self.kill()



class FakePowerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(images_dir / 'health_pack.png').convert_alpha()
        self.heal_amount = 15
        self.rect = self.image.get_rect()
        self.rect[0] = random.randint(100, 500)
        self.rect[1] = random.randint(100, 400)


# Setup variables
players = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
powerups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

clock = pygame.time.Clock()
running = True
game_over = False

def reset_game():
    global test, test2, players, projectiles, all_sprites, player_count, game_over, powerup, powerups, fpowerup, fpowerups
    player_count = 0
    game_over = False

    test = Player()
    test2 = Player()
    fpowerup = FakePowerup()
    powerup = Powerup()

    powerups = pygame.sprite.Group(powerup)
    fpowerups = pygame.sprite.Group(fpowerup)
    players = pygame.sprite.Group(test, test2)

    projectiles = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(test, test2, powerup, fpowerup )

reset_game()

def main():
    global clock, running, game_over
    while running:


        screen.fill((237, 229, 119))
        font = pygame.font.SysFont(None, 32)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False





        all_sprites.update()
        all_sprites.draw(screen)

        score_txt = font.render(f"Player 0 HP: {int(test.health)}", True, (38, 67, 112))
        screen.blit(score_txt, (20, 20))

        score_txt = font.render(f"Player 1 HP: {int(test2.health)}", True, (112, 38, 38))
        screen.blit(score_txt, (400, 20))


        pygame.display.flip()
        clock.tick(Settings.FPS)

        

        if game_over:
            print("Game Over!")
            pygame.time.delay(3500)
            reset_game()


    pygame.quit()

if __name__ == "__main__":
    main()
