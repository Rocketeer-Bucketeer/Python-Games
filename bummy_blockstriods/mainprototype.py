import pygame
import math

# Initialize Pygame
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bummy Blockstroids - Prototype")
clock = pygame.time.Clock()

# Player properties
player_pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
player_size = 50  # triangle size

def draw_player(surface, position, angle):
    # Triangle points (relative)
    points = [
        pygame.Vector2(0, -player_size),           # Tip
        pygame.Vector2(-player_size/2, player_size/2),  # Left
        pygame.Vector2(player_size/2, player_size/2),   # Right
    ]
    # Rotate points
    rotated = [p.rotate(angle) + position for p in points]
    pygame.draw.polygon(surface, WHITE, rotated)

# Game loop
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mouse to angle
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx, dy = mouse_x - player_pos.x, mouse_y - player_pos.y
    angle = math.degrees(math.atan2(dy, dx)) + 90  # <-- flipped

    # Draw player
    draw_player(screen, player_pos, angle)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
