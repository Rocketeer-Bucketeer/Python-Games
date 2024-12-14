""" Turtle in Pygame

We really miss the turtle module from Python's standard library. It was a great
way to introduce programming, so let's make something similar in PyGame, using
objects. 

"""
import math
import pygame

def event_loop():
    """Wait until the user closes the window."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

class Turtle:
    def __init__(self, screen, x: int, y: int):
        self.x = x
        self.y = y
        self.screen = screen
        self.angle = 0  # Angle in degrees, starting facing right
        self.pen_down = True  # By default, pen is down and drawing

    def forward(self, distance):
        """Move the turtle forward by a certain distance and draw if the pen is down."""
        radian_angle = math.radians(self.angle)

        start_x = self.x  # Save the starting position
        start_y = self.y

        # Calculate the new position displacement
        dx = math.cos(radian_angle) * distance
        dy = math.sin(radian_angle) * distance

        # Update the turtle's position
        self.x += dx
        self.y -= dy  # In Pygame, y coordinates grow downward

        # Draw the line if the pen is down
        if self.pen_down:
            pygame.draw.line(self.screen, black, (start_x, start_y), (self.x, self.y), 2)

    def left(self, angle):
        """Turn the turtle counterclockwise by the given angle."""
        self.angle = (self.angle + angle) % 360

    def right(self, angle):
        """Turn the turtle clockwise by the given angle."""
        self.angle = (self.angle - angle) % 360

    def penup(self):
        """Lift the pen so the turtle won't draw."""
        self.pen_down = False

    def pendown(self):
        """Put the pen down so the turtle will draw."""
        self.pen_down = True

    def position(self):
        """Print the current position of the turtle."""
        print(f"Current Position: ({self.x}, {self.y})")

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Turtle Style Drawing")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

screen.fill(white)
turtle = Turtle(screen, screen.get_width() // 2, screen.get_height() // 2)  # Start at the center of the screen

# Draw a square using turtle-style commands
for _ in range(4):
    turtle.forward(100)  # Move forward by 100 pixels
    turtle.right(90)
    turtle.forward(50)
    turtle.left(90)  # Turn right by 90 degrees

# Move the turtle and print its position
turtle.forward(100)
turtle.position()  # Prints the current position of the turtle

# Display the drawing
pygame.display.flip()

# Wait until the user closes the window
event_loop()

# Quit Pygame
pygame.quit()
