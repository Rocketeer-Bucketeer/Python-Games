import pygame
import math

# Initialize pygame
pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("better than v20, you should just use this instead haha but i guess i used v20 for it so um forget what i said why are you still reading this")


class V20rework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __mul__(self, scale_factor):
        # Scale both x and y components
        return V20rework(self.x * scale_factor, self.y * scale_factor)
    
    def __repr__(self):
        return f"V20rework({self.x}, {self.y})"
    
    def rotate(self, angle):
        radians = math.radians(angle)  # Convert angle to radians
        cos_angle = math.cos(radians)
        sin_angle = math.sin(radians)
        new_x = self.x * cos_angle - self.y * sin_angle
        new_y = self.x * sin_angle + self.y * cos_angle
        return V20rework(new_x, new_y) 
        # trigonometry magic
    
    def hypotenuse(self):
        return math.sqrt(self.x**2 + self.y**2)

# Creation of the triangle's sides


# Base of the triangle (along the x-axis)
base = V20rework(1, 1)
# Height of the triangle (along the y-axis)
height = V20rework(0, 1)
# Hypotenuse (diagonal)
diag = V20rework(1,1).rotate(45)
# Scale the vectors to make the triangle bigger
base_scaled = base * 200
height_scaled = height * 200
hypotenuse_scaled = diag * 200



origin = (100, 100)
base_end = (origin[0] + base_scaled.x, origin[1] + base_scaled.y)
height_end = (origin[0] + height_scaled.x, origin[1] + height_scaled.y)
hypotenuse_end = (origin[0] + hypotenuse_scaled.x, origin[1] + hypotenuse_scaled.y)


# Set up the points where we will draw the triangle

# Update display
pygame.display.flip()

# Game loop to draw the triangle
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw the right triangle
    pygame.draw.line(screen, (255, 0, 0), origin, base_end, 5)  # Base (Red)
    pygame.draw.line(screen, (0, 255, 0), origin, height_end, 5)  # Height (Green)
    pygame.draw.line(screen, (0, 0, 255), base_end, height_end, 5)  # Hypotenuse (Blue)
    print()
    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
