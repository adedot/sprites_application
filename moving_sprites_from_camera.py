"""
Moving Sprites from Pixy Camera
"""

import pygame
import random
import json
import requests


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# add yellow
# blue

colors = {1: RED, 2:GREEN, 3: BLUE}


# Create color mappings dictionary

# Add yellow


BASE_URL = "http://54.146.129.119:8080/"




class Block(pygame.sprite.Sprite):
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
        self.image.fill(color)


        self.block_id = block_id
        self.signature = signature
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

    def reset_pos(self):
        """ Reset position to the top of the screen, at a random x location.
        Called by update() or the main program loop if there is a collision.
        """
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, screen_width)

    def update(self):
        """ Called each frame. """

        url = BASE_URL + "blocks/updated/?block_id={}&signature={}".format(self.block_id, self.signature)

        r = requests.get(url)

        block_json = json.loads(r.text)

        self.rect.x = int(round(float(block_json['x'])))
        self.rect.y = int(round(float(block_json['y'])))

# def setBlock(block_json)
#     width = int(round(float(block_json['width'])))
#     height = int(round(float(block_json['height'])))
#     block = Block(BLACK, width, height)
#     x = int(round(float(block_json['x'])))
#     y = int(round(float(block_json['y'])))
#     block.rect.x = x
#     block.rect.y = y

#     return block


# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 400
screen_height = 300
screen = pygame.display.set_mode([screen_width, screen_height])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

#requests.delete(BASE_URL+'blocks/delete/')

# # Send a request to get the latest blocks
r = requests.get(BASE_URL+'blocks/latest/')
# dump the json into a dictionary
blocks = json.loads(r.text)

# Create the blocks
for number in range(len(blocks)):

    block_id = blocks[number]['block_id']
    signature = blocks[number]['signature']
    width = int(round(float(blocks[number]['width'])))
    height = int(round(float(blocks[number]['height'])))
    block = Block(colors[signature], width, height, block_id, signature)
    x = int(round(float(blocks[number]['x'])))
    y = int(round(float(blocks[number]['y'])))
    block.rect.x = x
    block.rect.y = y
    block_list.add(block)
    all_sprites_list.add(block)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the screen
    screen.fill(BLACK)

    # Calls update() method on every sprite in the list
    all_sprites_list.update()
    # To up date the position, make a call to the web service
    # to find the next position given the block id


    # Draw all the spites
    all_sprites_list.draw(screen)

    # Limit to 20 frames per second
    clock.tick(30)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()