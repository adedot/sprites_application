"""
Moving Sprites from Pixy Camera
"""

import pygame
import ujson as json
import serial
from pygame.transform import scale
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
LEFT_BARRIER = 43
RIGHT_BARRIER = 290

colors = {2: RED, 3:GREEN, 1: YELLOW, 4: BLUE }
color_names = {2: "RED", 3: "GREEN", 1: "YELLOW", 4: "BLUE"}

goal_list = [6,7]
BALL_SIZE = 15
# Create color mappings dictionary
# {2: "RED", 3: "GREEN", 1: "YELLOW", 5: "BLUE"}
#Keep track of score from color mappings dictionaries
score = { 1 : 0, 3: 0, 2: 0, 4: 0}

ball_id_list = []

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
ball_list = pygame.sprite.Group()
ball_hit_list_1 = pygame.sprite.Group()
ball_hit_list_2 = pygame.sprite.Group()


# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()


html_file = open('score.html', 'w')
html_file.write("""
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="1">
</head>
<body bgcolor="black">""")
html_file.write("\n<p>The Score is:\n")

for color in colors:
        html_file.write("\n<p style=\"color:{}\">    {} has {}</p>" .format(str(color_names[color]).lower(),color_names[color], score[color]))

html_file.write("""</body>
</html>""")
html_file.close()
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


# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 320*3
screen_height = 220*3
# screen=pygame.display.set_mode((640,480),0,24)
screen = pygame.display.set_mode([screen_width, screen_height],HWSURFACE|DOUBLEBUF|RESIZABLE)
# surface = pygame.display.get_surface()
# pygame.transform.scale(surface, (800, 800))
# screen = pygame.display.set_mode([800, 800],HWSURFACE|RESIZABLE)

# screen.blit(surface,(800, 800), (0,0))
# number_screen = pygame.display.set_mode([screen_width, screen_height])

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
    html_file = open('score.html', 'w+')
    html_file.write("""
<!DOCTYPE html>
<html>
<head>
  <meta http-equiv="refresh" content="1">
</head>
<body bgcolor="black">""")
    html_file.write("\n<p style=\"color:{}\">    {} now has {}</p>" .format(str(color_names[signature]).lower(), color_names[signature], score[signature]))
    html_file.write("\n<p>    Score now is:")
    for color in colors:
        html_file.write("\n<p style=\"color:{}\">    {} has {}</p>" .format(str(color_names[color]).lower(),color_names[color], score[color]))
    html_file.write("""</body>
</html>""")
    html_file.close()


def create_new_ball(ball_data):
    ball = Ball(colors[signature], BALL_SIZE, BALL_SIZE, ball_data['block_id'], ball_data['signature'])
    ball.rect.x = ball_data['x'] * 3
    ball.rect.y = ball_data['y'] * 3
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
serial_data.flushInput()
serial_data.flushOutput()
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # if event.type == VIDEORESIZE:
        #     # The main code that resizes the window:
        #     # (recreate the window with the new size)
        #     surface = pygame.display.set_mode((event.w, event.h),
        #                                   pygame.RESIZABLE)

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

            if block_id in ball_id_list and signature not in goal_list and LEFT_BARRIER < ball_data['x'] < RIGHT_BARRIER:
                # delete ball
                for old_ball in ball_list:
                    if old_ball.block_id == block_id:
                        if old_ball.rect.x != ball_data['x'] and old_ball.rect.y != ball_data['y']:
                            old_ball.kill()
                            create_new_ball(ball_data)
                            break
                        break

            else:
                if signature not in goal_list and LEFT_BARRIER < ball_data['x'] < RIGHT_BARRIER:
                    create_new_ball(ball_data)

        except ValueError as msg:
            pass
            # print(line.strip(' \t\n\r'))
            # print("{}".format(msg))

    # # See if the player block has collided with anything.
    ball_hit_list_1 = pygame.sprite.spritecollide(line_1, ball_list, True)
    ball_hit_list_2 = pygame.sprite.spritecollide(line_2, ball_list, True)
    # Check the list of collisions.
    for ball in ball_hit_list_1:
        # print("Ball {} has crossed the left line".format(ball.block_id))
        update_score(ball.signature)
        # ball_hit_list_1.remove(ball.block_id)
        ball_id_list.remove(ball.block_id)

    #     # update the score for the ball

    for ball in ball_hit_list_2:
        # print("Ball {} has crossed the right line".format(ball.block_id))
        update_score(ball.signature)
        # ball_hit_list_2.remove(ball.block_id)
        ball_id_list.remove(ball.block_id)

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Limit to 50 frames per second
    clock.tick(50)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()