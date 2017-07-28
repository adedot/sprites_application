import pygame
from score import *

from colors import *


# Barriers
LEFT_BARRIER = 43
RIGHT_BARRIER = 290

colors = {2: RED, 3:GREEN, 1: YELLOW, 4: BLUE }
# score = { 1 : 0, 3: 0, 2: 0, 4: 0}

BALL_SIZE = 15

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
        self.image = pygame.Surface([width*3, height*3])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x * 3
        self.rect.y = y * 3


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
        self.image = pygame.Surface([width*3, height*3])
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
        pygame.draw.ellipse(self.image,color, [0, 0, width*3, height*3])

def create_new_ball(ball_data, ball_id_list, ball_list, all_sprites_list):
    block_id = ball_data['block_id']
    signature = ball_data['signature']
    ball = Ball(colors[signature], BALL_SIZE, BALL_SIZE, ball_data['block_id'], ball_data['signature'])
    ball.rect.x = ball_data['x'] * 3
    ball.rect.y = ball_data['y'] * 3
    ball_list.add(ball)

    if ball_data['block_id'] not in ball_id_list:
        ball_id_list.append(block_id)
    all_sprites_list.add(ball)


def create_ball(ball_data, ball_id_list, ball_list, goal_list, all_sprites_list):
    block_id = ball_data['block_id']
    signature = ball_data['signature']

    if block_id in ball_id_list and signature not in goal_list and LEFT_BARRIER < ball_data['x'] < RIGHT_BARRIER:
        # delete ball
        for old_ball in ball_list:
            if old_ball.block_id == block_id:
                if old_ball.rect.x != ball_data['x'] and old_ball.rect.y != ball_data['y']:
                    old_ball.kill()
                    create_new_ball(ball_data, ball_id_list, ball_list, all_sprites_list)
                    break
                break
    else:
        if signature not in goal_list and LEFT_BARRIER < ball_data['x'] < RIGHT_BARRIER:
            create_new_ball(ball_data, ball_id_list, ball_list, all_sprites_list)

def check_ball_collisions(line_1, line_2, ball_list, ball_id_list):
    ball_hit_list_1 = pygame.sprite.spritecollide(line_1, ball_list, True)
    ball_hit_list_2 = pygame.sprite.spritecollide(line_2, ball_list, True)
    # Check the list of collisions.
    for ball in ball_hit_list_1:
        # print("Ball {} has crossed the left line".format(ball.block_id))
        update_score(ball.signature)
        # ball_hit_list_1.remove(ball.block_id)
        ball_id_list.remove(ball.block_id)
        # update the score for the ball

    for ball in ball_hit_list_2:
        # print("Ball {} has crossed the right line".format(ball.block_id))
        update_score(ball.signature)
        # ball_hit_list_2.remove(ball.block_id)
        ball_id_list.remove(ball.block_id)