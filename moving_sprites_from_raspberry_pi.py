from pixy import *
from ctypes import *
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
# Pixy Python SWIG get blocks example #

print ("Pixy Python SWIG Example -- Get Blocks")

# Initialize Pixy Interpreter thread #
pixy_init()

class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

blocks = BlockArray(100)
frame  = 0

# Wait for blocks #
while 1:
  for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
  # Clear the screen
  screen.fill(BLACK)

  count = pixy_get_blocks(100, blocks)

  if count > 0:
    # Blocks found #
    print('frame %3d:' % (frame))
    frame = frame + 1
    for index in range (0, count):
      print('[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d]' % (blocks[index].type, blocks[index].signature, blocks[index].x, blocks[index].y))
      blocks[index]["block_id"] = index
      create_ball(blocks[index], ball_id_list, ball_list, goal_list,all_sprites_list)
      
  check_ball_collisions(line_1, line_2, ball_list, ball_id_list)

  # Draw all the spites
  all_sprites_list.draw(screen)

  # Limit to 50 frames per second
  clock.tick(50)

  # Go ahead and update the screen with what we've drawn.
  pygame.display.flip()

pygame.quit()