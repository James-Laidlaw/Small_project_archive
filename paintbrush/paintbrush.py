# this is a simple paint software, the user controls a paintbrush using the arrow keys, leaving a trail in the window
# of a specified color chosen from blue, green, red, yellow, and black

import pygame


def main():
    # initialize pygame -- this is required for rendering fonts
    pygame.init()

    # create the window and set its size to 500 width and 400 height
    size = (500, 400)
    screen = pygame.display.set_mode(size)

    # set the title of the window
    pygame.display.set_caption("Painting")

    # start the game
    game = Game(screen)
    game.play()


class Game:
    # the types of attributes that a game might have
    # --- general to all games
    # screen objects are being drawn to
    # background color
    # game clock
    # FPS limit
    # is the game over? (continue_game)
    # ---specific to painting:
    # brush
    # available colors

    # Game_screen is a pygame value containing information relating to the window the game will be played in
    def __init__(self, game_screen):

        # --- attributes that are general to all games
        self.screen = game_screen
        self.bg_color = pygame.Color("black")
        self.game_clock = pygame.time.Clock()
        self.FPS = 60
        self.continue_game = True
        self.close_clicked = False

        # --- attributes that are specific to paintbrush

        # game objects that are specific to paintbrush

        # establish variables for paintbrush and create the paintbrush object
        brush_color_controls = (pygame.K_b, pygame.K_g, pygame.K_r, pygame.K_y, pygame.K_SPACE)
        brush_dimensions = [10, 10]
        brush_movement_controls = (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)

        # find coordinates needed to place brush in center of screen
        screen_dimensions = self.screen.get_size()
        screen_center = [screen_dimensions[0] // 2, screen_dimensions[1] // 2]
        brush_pos = [screen_center[0] - brush_dimensions[0], screen_center[1] - brush_dimensions[1]]

        # create brush object
        self.brush = Brush(brush_dimensions, brush_pos, self.screen, brush_movement_controls, brush_color_controls)

    # This method is responsible for managing all events happening every frame
    def play(self):

        # Play the game until the player presses the close box.
        while not self.close_clicked:

            # check for player input
            self.handle_events()

            # draw objects to window
            self.draw()

            # update the game state
            self.update()

            # wait until the end of allotted frame time before repeating, effectively capping frame rate
            self.game_clock.tick(self.FPS)

    # this method is responsible for handling all user input into the game and routing to the correct method
    def handle_events(self):

        # Checks for new events generated by user input, and then change our
        # game state appropriately.
        for event in pygame.event.get():

            # check if player hit the "x" button on the window, and close the game if so
            if event.type == pygame.QUIT:
                self.close_clicked = True

            # route player control inputs to the correct brush control method
            if event.type == pygame.KEYUP:
                self.brush.key_up_movement_handler(event)

            if event.type == pygame.KEYDOWN:
                if event.key in self.brush.get_move_controls():
                    self.brush.key_down_movement_handler(event)
                if event.key in self.brush.get_color_controls():
                    self.brush.key_down_color_handler(event)

    # this method is responsible for drawing all objects meant to be visible to the window
    # in order to achieve a "painting" effect, the screen is purposefully not cleared every frame, allowing afterimages
    # of the brush to form
    def draw(self):
        # draws all game objects to screen

        # draw our brush to the screen
        self.brush.draw()

        # render all drawn objects to the screen
        pygame.display.flip()

    # this method is responsible for updating and monitoring the state of all objects in the window
    def update(self):

        # check for collisions
        self.collision_check()

        # move the game objects
        self.brush.move()

    # this method runs all the collision check methods
    def collision_check(self):
        self.brush.brush_wall_collision_check()


# this class represents a 'brush' in painting
# a brush is a rectangle
# a brush can move within the screen as directed by player inputs
# a brush can be apply blue, green, yellow, red, or black color to the screen depending on the color of the brush
# a brush's color can be changed through user inputs, pressing the first letter of the color on the keyboard
# if the color is black, the space bar is used instead
class Brush:
    # brush_dimensions is a list containing two integers for the width (index 0) and height (index 1) of the brush
    # brush_top_left is a list containing the starting coordinates of the brush's top left corner in [x, y] format
    # screen is a pygame screen value indicating which screen the brush will be printed to
    # movement_controls is a tuple containing the  keys to move the brush in (up, down, left, right) format
    # color_controls is a tuple containing the controls to change the brush's color. the color corresponds to the color
    # at the same index in self.colors
    def __init__(self, brush_dimensions, brush_top_left, screen, movement_controls, color_controls):
        red = pygame.Color('red')
        green = pygame.Color('green')
        blue = pygame.Color('blue')
        yellow = pygame.Color('yellow')
        black = pygame.Color('black')
        self.colors = [blue, green, red, yellow, black]
        self.color_controls = color_controls
        self.color = self.colors[2]  # this sets the brush's default color to red
        self.velocity = [0, 0]
        self.screen = screen
        self.movement_controls = movement_controls
        self.up_control = movement_controls[0]
        self.down_control = movement_controls[1]
        self.left_control = movement_controls[2]
        self.right_control = movement_controls[3]
        self.rectangle = pygame.Rect(brush_top_left[0], brush_top_left[1], brush_dimensions[0], brush_dimensions[1])

    # this method offsets the brush using "rect"'s inbuilt "move" function by passing in x and y velocity
    def move(self):
        self.rectangle = self.rectangle.move(self.velocity[0], self.velocity[1])

    # event is a pygame "event" type variable containing information about player interaction with the game window

    # this method handles events relating to player inputs meant to change the color of the brush
    # the method checks what control was pressed, and changes the color of the brush accordingly
    def key_down_color_handler(self, event):
        input_key = event.key

        # ensure that the event is relevant to changing the color of the brush before processing it
        if input_key in self.color_controls and event.type == pygame.KEYDOWN:

            # find the index of the key on the control list, then set the brush color to the color at that index
            color_index = self.color_controls.index(input_key)
            self.color = self.colors[color_index]

    # This method checks for any possible collisions between the walls and the brush
    # If any are found, the brush's velocity is set to 0 for the axis, preventing it from leaving the window
    def brush_wall_collision_check(self):

        screen_dimensions = self.screen.get_size()

        # go through collisions in x and y axis separately, axis == 0 is x axis, axis == 1 is y axis
        for axis in range(2):

            # find relevant side coordinates
            if axis == 0:
                sides = [self.rectangle.left, self.rectangle.right]
            else:  # if axis == 1
                sides = [self.rectangle.top, self.rectangle.bottom]

            # check if brush is colliding with the walls on current axis, If so, set velocity for current axis to 0
            if sides[0] < 0 and self.velocity[axis] < 0:
                self.velocity[axis] = 0
            elif sides[1] > screen_dimensions[axis] and self.velocity[axis] > 0:
                self.velocity[axis] = 0

    # This method is responsible for drawing the brush specified in it's call
    def draw(self):

        # Draw the brush onto the game's window
        pygame.draw.rect(self.screen, self.color, self.rectangle)

    # event is a pygame "event" type variable containing information about player interaction with the game window

    # this method checks if the event passed into it is a keystroke (up) relating to the movement_controls for
    # the brush specified in it's call. If so, it alters the brush's velocity accordingly
    def key_up_movement_handler(self, event):

        # only reduce speed to 0 if the button released correlates to the current direction the brush is moving in
        # this leads to more pleasant movement_controls, but is not necessary for functionality

        # if brush is moving up and up key is released, set vertical velocity to 0
        if event.key == self.up_control and self.velocity[1] < 0:
            self.velocity[1] = 0

        # If brush is moving down and down key is released, set vertical velocity to 0
        if event.key == self.down_control and self.velocity[1] > 0:
            self.velocity[1] = 0

        # if brush is moving left and left key is released, set horizontal velocity to 0
        if event.key == self.left_control and self.velocity[0] < 0:
            self.velocity[0] = 0

        # if brush is moving right and right key is released, set horizontal velocity to 0
        if event.key == self.right_control and self.velocity[0] > 0:
            self.velocity[0] = 0

    # event is a pygame "event" type variable containing information about player interaction with the game window

    # this method checks if the event passed into it is a keystroke (down) relating to the movement_controls for
    # the brush specified in it's call. If so, it alters the brush's velocity accordingly
    def key_down_movement_handler(self, event):

        brush_speed = 4  # pixels/frame (60 fps default)

        # if the key pressed is the assigned up key, set vertical velocity to -1 * brush_speed (up)
        if event.key == self.up_control:
            self.velocity[1] = -1 * brush_speed

        # if the key pressed is the assigned down key, set vertical velocity to brush_speed (down)
        if event.key == self.down_control:
            self.velocity[1] = brush_speed

        # if the key pressed is the assigned left key, set vertical velocity to -1 * brush_speed (left)
        if event.key == self.left_control:
            self.velocity[0] = -1 * brush_speed

        # if the key pressed is the assigned down key, set vertical velocity to brush_speed (right)
        if event.key == self.right_control:
            self.velocity[0] = brush_speed

    # this method returns the movement controls of the brush as a tuple
    def get_move_controls(self):
        return self.movement_controls

    # this method returns the color controls of the brush as a tuple
    def get_color_controls(self):
        return self.color_controls


main()