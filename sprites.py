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


def create_new_ball(ball_data):
    ball = Ball(colors[signature], BALL_SIZE, BALL_SIZE, ball_data['block_id'], ball_data['signature'])
    ball.rect.x = ball_data['x'] * 3
    ball.rect.y = ball_data['y'] * 3
    ball_list.add(ball)
    if ball_data['block_id'] not in ball_id_list:
        ball_id_list.append(block_id)
    all_sprites_list.add(ball)