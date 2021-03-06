"""
Moving Sprites from Pixy Camera
"""

import pygame
import ujson as json
import serial
from pygame.transform import scale
from pygame.locals import *
from colors import *

from game_utilities import *


colors = {2: RED, 3:GREEN, 1: YELLOW, 4: BLUE }
color_names = {2: "RED", 3: "GREEN", 1: "YELLOW", 4: "BLUE"}

goal_list = [6,7]

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
        html_file.write("\n<p style=\"color:{};font-size:40px;\">    {} has {}</p>" .format(str(color_names[color]).lower(),color_names[color], score[color]))

html_file.write("""</body>
</html>""")
html_file.close()



# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 320*3
screen_height = 220*3
screen = pygame.display.set_mode([screen_width, screen_height],HWSURFACE|DOUBLEBUF|RESIZABLE)

# # Create a white blocks
line_1 = Line(PURPLE, 10, 500, LEFT_BARRIER, 0)
line_2 = Line(PURPLE, 10, 500, RIGHT_BARRIER, 0)
all_sprites_list.add(line_1)
all_sprites_list.add(line_2)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


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

    # Clear the screen
    screen.fill(BLACK)

    line = serial_data.readline();
    line = line.decode("utf-8") #ser.readline returns a binary, convert to string
    print(line.strip(' \t\n\r'))
    if line.strip(' \t\n\r'):
        try:
            ball_data = json.loads(line.strip(' \t\n\r')) # needed to get data as json object
            # create ball
            create_ball(ball_data, ball_id_list, ball_list, goal_list,all_sprites_list)

        except ValueError as msg:
            pass

    # # See if the player block has collided with anything.

    check_ball_collisions(line_1, line_2, ball_list, ball_id_list)

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Limit to 50 frames per second
    clock.tick(50)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()