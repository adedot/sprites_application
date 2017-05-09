"""
Moving Sprites from Pixy Camera
"""

import pygame
import random
import ujson as json
import serial
import time
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
PURPLE = (75,0,130)

# Barriers
LEFT_BARRIER = 45
RIGHT_BARRIER = 290

colors = {2: RED, 3:GREEN, 1: YELLOW, 5: BLUE }
color_names = {2: "RED", 3: "GREEN", 1: "YELLOW", 5: "BLUE"}

goal_list = [6,7]
BALL_SIZE = 15
# Create color mappings dictionary
# {2: "RED", 3: "GREEN", 1: "YELLOW", 5: "BLUE"}
#Keep track of score from color mappings dictionaries
score = { 1 : 0, 3: 0, 2: 0, 5: 0}

ball_id_list = []

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
ball_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# Used to create a thick line
class Line(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, color, width, height, x, y):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, color, width, height, block_id, signature):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)


        # Set the block id and signature to be used later
        self.block_id = block_id
        self.signature = signature
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        pygame.draw.ellipse(self.image,color, [0, 0, width, height])


def getUpdatedBalls():
    pass
    #

def deleteBlock(block):
    block.kill()
    update_score(block.signature)

# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 320
screen_height = 220
screen = pygame.display.set_mode([screen_width, screen_height],HWSURFACE|DOUBLEBUF|RESIZABLE)

# number_screen = pygame.display.set_mode([screen_width, screen_height])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# # Create a white blocks
line_1 = Line(PURPLE, 10, 500, LEFT_BARRIER, 0)
line_2 = Line(PURPLE, 10, 500, RIGHT_BARRIER, 0)
all_sprites_list.add(line_1)
all_sprites_list.add(line_2)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def update_score(signature):
    score[signature] += 1
    print("    {} now has {}" .format(color_names[signature], score[signature]))
    print("    Score now is:")
    for color in colors:
        print("    {} has {}" .format(color_names[color], score[color]))


def create_new_ball(ball_data):
    ball = Ball(colors[signature], BALL_SIZE, BALL_SIZE, ball_data['block_id'], ball_data['signature'])
    ball.rect.x = ball_data['x']
    ball.rect.y = ball_data['y']
    ball_list.add(ball)
    if ball_data['block_id'] not in ball_id_list:
        ball_id_list.append(block_id)
    all_sprites_list.add(ball)
# Serial Information
serial_port = '/dev/cu.usbmodem1421'
baud_rate = 9600 #In arduino, Serial.begin(baud_rate)

serial_data = serial.Serial(serial_port, baud_rate)


# clear data
serial_data.reset_input_buffer()
serial_data.reset_output_buffer()
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the screen
    screen.fill(BLACK)

    line = serial_data.readline();
    line = line.decode("utf-8") #ser.readline returns a binary, convert to string
    # print(line.strip(' \t\n\r'))
    if line.strip(' \t\n\r'):
        try:
            ball_data = json.loads(line.strip(' \t\n\r')) # needed to get data as json object
            block_id = ball_data['block_id']
            signature = ball_data['signature']

            if block_id in ball_id_list and signature not in goal_list:
                # delete ball
                for old_ball in ball_list:
                    if old_ball.block_id == block_id:
                        if old_ball.rect.x != ball_data['x'] and old_ball.rect.y != ball_data['y']:
                            old_ball.kill()
                            create_new_ball(ball_data)
                        break
            else:
                if signature not in goal_list:
                    print(line.strip(' \t\n\r'))
                    print(ball_id_list)
                    print(ball_list)
                    print("Block id: {}".format(block_id))
                    print("Adding new ball")
                    create_new_ball(ball_data)

        except ValueError as msg:
            print(line.strip(' \t\n\r'))
            print("{}".format(msg))

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Limit to 50 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()