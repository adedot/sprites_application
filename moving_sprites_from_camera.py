"""
Moving Sprites from Pixy Camera
"""

import pygame
import random
import ujson as json
import requests
from requests.adapters import HTTPAdapter

import time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Barriers
LEFT_BARRIER = 25
RIGHT_BARRIER = 300

colors = {1: RED, 3:GREEN}
color_names = {1: "RED", 3: "GREEN", 2: "BLUE"}

BALL_SIZE = 10
# Create color mappings dictionary
# 1: RED, 3:GREEN
#Keep track of score
score = { 1 : 0, 3: 0}

block_id_list = []

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()

# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()


BASE_URL = "http://54.146.129.119:8080/"

class Block(pygame.sprite.Sprite):
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


    # def reset_pos(self):
    #     """ Reset position to the top of the screen, at a random x location.
    #     Called by update() or the main program loop if there is a collision.
    #     """
    #     self.rect.x= random.randrange(-300, -20)
    #     self.rect.y = random.randrange(0, screen_width)

    def update(self):
        """ Called each frame. """

        try:
            url = BASE_URL + "blocks/updated/?block_id={}&signature={}".format(self.block_id, self.signature)

            # time.sleep(0.5)
            r = requests.get(url)

            block_json = json.loads(r.text)

            if LEFT_BARRIER < block_json['x'] < RIGHT_BARRIER:
                if not (self.rect.x == block_json['x'] and self.rect.y == block_json['y']):
                    self.rect.x = block_json['x']
                    self.rect.y = block_json['y']
            else:
                deleteBlock(self)

        except requests.exceptions.ConnectionError:
            pass
        except ValueError:
            print("No Expected value for block_id {} and signature {}".format(self.block_id, self.signature))
            self.kill()

def getLatestBalls():

    # # Send a request to get the latest blocks
    blocks_request = requests.get(BASE_URL+'blocks/latest/')
    # dump the json into a dictionary
    blocks = json.loads(blocks_request.text)

    # Create the blocks
    for number in range(len(blocks)):

        block_id = blocks[number]['block_id']
        signature = blocks[number]['signature']
        if LEFT_BARRIER < blocks[number]['x'] < RIGHT_BARRIER and block_id not in block_id_list:
            print(blocks[number]['x'])
            width = 25
            height = 25
            block = Ball(colors[signature], width, height, block_id, signature)
            block.rect.x = blocks[number]['x']
            block.rect.y = blocks[number]['y']
            block_list.add(block)
            block_id_list.append(block_id)
            all_sprites_list.add(block)
        else:
            print(blocks[number])
            try:

                url = BASE_URL + "blocks/delete/?block_id={}&signature={}".format(block.block_id, block.signature)
                r = requests.delete(url)
            except requests.exceptions.ConnectionError:
                pass
            except ValueError:
                print("No Expected value for block_id {} and signature {} for ".format(self.block_id, self.signature))

def getUpdatedBalls(): 
    pass
    # 



def deleteBlock(block):
    try:
        url = BASE_URL + "blocks/delete/?block_id={}&signature={}".format(block.block_id, block.signature)
        r = requests.delete(url)
        block.kill()
        update_score(block.signature)
    except requests.exceptions.ConnectionError:
        pass

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

# To up date the position, make a call to the web service
# to find the next position given the block id
getLatestBalls()


# Create a white blocks
line_1 = Block(WHITE, 20, 500, LEFT_BARRIER, 0)
line_2 = Block(WHITE, 20, 500, RIGHT_BARRIER, 0)
all_sprites_list.add(line_1)
all_sprites_list.add(line_2)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def update_score(signature):
    score[signature] += 1
    print("{} now has {}" .format(color_names[signature], score[signature]))
    print("Score now is:")
    for color in colors:
        print("{} has {}" .format(color_names[color], score[color]))


# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Clear the screen
    screen.fill(BLACK)

    # Calls update() method on every sprite in the list
    all_sprites_list.update()
    # for sprite in block_list:
    #     print(sprite.block_id)
    #     print(sprite.signature)
    # getLatestBalls()

    # See if the player block has collided with anything.
    ball_hit_list_1 = pygame.sprite.spritecollide(line_1, block_list, True)
    ball_hit_list_2 = pygame.sprite.spritecollide(line_2, block_list, True)

    # Delete all the boys in the hit list
    # Check the list of collisions.
    for block in ball_hit_list_1:
        deleteBlock(block)

    for block in ball_hit_list_2:
        deleteBlock(block)

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Limit to 10 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()