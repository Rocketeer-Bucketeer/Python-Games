import pygame
import math
import time  # To use time tracking for the combo reset
import random
# Initialize Pygame
pygame.init()

# Set up the screen
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 470
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("cool game yes yes very cool indeed")

# Colors
FLASH = (150,150,150)
WHITE = (255, 255, 255)
BLUE = (132, 175, 245)
BLACK = (48, 48, 48)
RED = (255, 0, 0)
YELLOW = (235, 174, 52)
GREEN = (17, 107, 14)
BLUE = (59, 73, 196)

bg_color = BLACK

# Player settings (Red ball)
player_radius = 15
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2
ball_velocity = [0, 0]

# Stationary ball settings
stationary_radius = 50
stationary_x = 500
stationary_y = 0

# Physics settings
gravity = 1
friction = 0.9 # Air resistance to slow down the ball

# Game variables
dragging = False
drag_start_x = 0
drag_start_y = 0
score = 0
last_hit_time = time.time()  # Start the timer when the game begins
combo_timeout = 2  # Seconds before combo resets

# Game clock
clock = pygame.time.Clock()

# Font for the score
font = pygame.font.SysFont("Arial", 30)



# Function to handle collision with the stationary ball
def handle_collision():
    global ball_velocity, player_x, player_y, score, last_hit_time, bg_color, stationary_x, stationary_y  # Include score and last_hit_time in global variables
    # Calculate the vector from the stationary ball to the player
    dx = player_x - stationary_x
    dy = player_y - stationary_y
    distance = math.sqrt(dx**2 + dy**2)

    # Check for collision
    if distance < player_radius + stationary_radius:
        # Normalize the collision vector
        normal_x = dx / distance
        normal_y = dy / distance
        
        # Increment score and reset the timer every time a collision occurs
        score += 1
        stationary_x = random.randint(1, 500)
        stationary_y = random.randint(100, 300)



        last_hit_time = time.time()  # Reset the combo timer
        
        # Dot product of the velocity and the normal vector (to calculate the reflection)
        velocity_dot_normal = ball_velocity[0] * normal_x + ball_velocity[1] * normal_y
        
        # Reflect the velocity
        ball_velocity[0] -= 2 * velocity_dot_normal * normal_x
        ball_velocity[1] -= 2 * velocity_dot_normal * normal_y
        print(ball_velocity)
        # Position the player ball outside the stationary ball to avoid sticking
        overlap = player_radius + stationary_radius - distance
        player_x += normal_x * overlap
        player_y += normal_y * overlap

        bg_color = FLASH

# Function to get the grade based on the combo score
def get_grade(combo_score):
    if combo_score >= 500:
        return "SSS", (255, 215, 0)  # Gold for SSS
    elif combo_score >= 250:
        return "SS", (255, 0, 0)  # Red for SS
    elif combo_score >= 100:
        return "S", (0, 255, 0)  # Green for S
    elif combo_score >= 10:
        return "A", (0, 0, 255)  # Blue for A
    elif combo_score >= 5:
        return "B", (255, 165, 0)  # Orange for B
    elif combo_score >= 2:
        return "C", (255, 255, 0)  # Yellow for C
    elif combo_score >= 1:
        return "D", (128, 128, 128)  # Gray for D
    else:
        return "F", (128, 0, 0)  # Dark Red for F

# Trajectory of the ball
def draw_trajectory(start_x, start_y, velocity_x, velocity_y, screen):
    steps = 30  # Increased the number of points to extend the trajectory
    time_step = 0.1  # Increased the time step to make the trajectory longer
    trajectory_points = []
    
    for i in range(steps):
        time_passed = i * time_step
        x = start_x + velocity_x * time_passed
        y = start_y + velocity_y * time_passed + 0.5 * gravity * time_passed**2
        if x > 0 and x < SCREEN_WIDTH and y > 0 and y < SCREEN_HEIGHT:
            trajectory_points.append((x, y))
    
    for point in trajectory_points:
        pygame.draw.circle(screen, YELLOW, (int(point[0]), int(point[1])), 3)  # Draw each point of the trajectory

# Game loop
running = True
pause = False
while running:
    # Fill the screen with black
    screen.fill(bg_color)

    if bg_color != BLACK:
        pause = True
        bg_color = BLACK

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                
                friction = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                friction = 0.9
        if event.type == pygame.MOUSEBUTTONDOWN:
            # drag when clicked on ball

            mouse_x, mouse_y = pygame.mouse.get_pos()
            dragging = True
            drag_start_x, drag_start_y = mouse_x, mouse_y
        if event.type == pygame.MOUSEBUTTONUP:
            # Release the ball 
            if dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Calculate velocity 
                delta_x = mouse_x - drag_start_x
                delta_y = mouse_y - drag_start_y
                ball_velocity = [delta_x * 0.25, delta_y * 0.25]  # Adjust sensitivity to improve accuracy
                dragging = False
        

    # Update ball physics if not dragging
    if not dragging:
        # Apply gravity to velocity
        ball_velocity[1] += gravity
        
        # Update position based on velocity
        player_x += ball_velocity[0]
        player_y += ball_velocity[1]
        
        # Apply friction to slow down the ball
        ball_velocity[0] *= friction
        ball_velocity[1] *= friction
        
        # Boundary collisions: bounce the ball off the edges
        if player_x - player_radius < 0 or player_x + player_radius > SCREEN_WIDTH:
            ball_velocity[0] *= -1  # Invert horizontal velocity
            player_x = max(player_radius, min(player_x, SCREEN_WIDTH - player_radius))  # Keep ball within bounds
        
        if player_y - player_radius < 0 or player_y + player_radius > SCREEN_HEIGHT:
            ball_velocity[1] *= -1  # Invert vertical velocity
            player_y = max(player_radius, min(player_y, SCREEN_HEIGHT - player_radius))  # Keep ball within bounds
        
        # Handle collision with the stationary ball
     

        handle_collision()

    # Reset combo if time since last hit exceeds the timeout threshold
    if time.time() - last_hit_time > combo_timeout:
        score = 0  # Reset score if timeout exceeded

    # Get the letter grade and color based on the score
    grade, grade_color = get_grade(score)

    # Draw the stationary ball (large ball)
    pygame.draw.circle(screen, RED, (stationary_x, stationary_y), stationary_radius)

    # Draw the red ball (player ball)
    pygame.draw.circle(screen, BLUE, (int(player_x), int(player_y)), player_radius)

    # Show score and grade
    score_text = font.render(f"Combo: {score}X", True, WHITE)
    grade_text = font.render(f"Grade: {grade}", True, grade_color)  

    
    screen.blit(score_text, (10, 10))
    screen.blit(grade_text, (10, 40))

    # Draw the drag trajectory
    if dragging:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        delta_x = mouse_x - drag_start_x
        delta_y = mouse_y - drag_start_y
        draw_trajectory(player_x, player_y, delta_x * 0.25, delta_y * 0.25, screen)

    # Update the display
    pygame.display.flip()

    # Frame rate
    if pause:
        pygame.time.delay(100)
        pause = False
    clock.tick(60)

# Quit Pygame
pygame.quit()
