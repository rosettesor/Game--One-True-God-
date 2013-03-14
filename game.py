import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 9
GAME_HEIGHT = 9

#### Put class definitions here ####

# WHAT DO I WANT THE GAME TO DO?
# IT IS A GAME TO COLLECT 3 NICHOLAS CAGE'S --> ONE TRUE GOD
# THERE WILL BE OTHER POSSIBLE "GODS" WHICH WILL NOT COUNT
# PLAYER CAN MOVE ROCKS TO ACCESS NICHOLAS CAGE
# AFTER COLLECTING ALL 3, DOOR IS UNLOCKED/OPENED

class MoveRock(GameElement):
    IMAGE = "Rock"
    SOLID = True

    def interact(self, player):
        del_x = player.x - self.x
        del_y = player.y - self.y
        next_x = self.x - del_x
        next_y = self.y - del_y

        if -1 < next_x < 9 and -1 < next_y < 9:

            existing_el = GAME_BOARD.get_el(next_x, next_y)

            if existing_el is None or not existing_el.SOLID:
            # If there's nothing there_or_ if the existing element, is not solid, walk through
                GAME_BOARD.del_el(self.x, self.y)
                self.x = next_x
                self.y = next_y
                GAME_BOARD.set_el(next_x, next_y, self)
                self.SOLID = False
                # player.sound.play
            # else:
            #     self.SOLID = True

class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True

class NicC(GameElement):
    IMAGE = "NicCage"
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        player.sound.play()
        GAME_BOARD.draw_msg("Success! You found him! You have %d Nicholas Cage(s)!" % (len(player.inventory)))

class Keanu(GameElement):
    IMAGE = "keanu"

    def interact(self, player):
        GAME_BOARD.draw_msg("Woops! This is NOT the One-True-God. Keep searching.")
        SOLID = False

class Grumpy(GameElement):
    IMAGE = "Cat"

    def interact(self, player):
        GAME_BOARD.draw_msg("Woops! This is NOT the One-True-God. Keep searching.")
        SOLID = False

class Character(GameElement):
    IMAGE = "EnemyBug"

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None

    def __init__(self):
        GameElement.__init__(self)
        self.sound = pyglet.resource.media("explosion.wav", streaming=False)
        self.inventory = []

class Door_closed(GameElement):
    IMAGE = "DoorClosed"

    def interact(self, player):
        if (len(player.inventory)) < 3:
            self.SOLID = True
            GAME_BOARD.draw_msg("This door is locked. You must collect at least 3 One-True-God's to unlock it.")
        if (len(player.inventory)) >= 3:
            class Door_opened(Door_closed):
                self.sprite = pyglet.sprite.Sprite(pyglet.resource.image("Door Tall Open.png"))
                self.SOLID = True
                GAME_BOARD.draw_msg("Congratulations! You have unlocked the door! THE END")

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    rock_positions = [
		(3,2),
		(2,4),
        (3,3),
        (0,8),
        (6,8),
        (8,4),
	]

    rocks = []
    for pos in rock_positions:
		rock = Rock()
		GAME_BOARD.register(rock)
		GAME_BOARD.set_el(pos[0], pos[1], rock)
		rocks.append(rock)

    move_rock_positions = [
        (7,3),
        (1,7),
        (3,1),
        (4,0),
        (2,8),
        (7,5),
        (7,1)
    ]

    move_rocks = []
    for pos in move_rock_positions:
        move_rock = MoveRock()
        GAME_BOARD.register(move_rock)
        GAME_BOARD.set_el(pos[0], pos[1], move_rock)
        move_rocks.append(move_rock)

    global PLAYER
    PLAYER = Character()
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2, 2, PLAYER)

    wall_positions = [
        (0,0),
        (1,0),
        (2,0),
        (3,2),
        (2,5),
        (3,3),
        (4,5),
        (4,6),
        (4,7),
        (3,6),
        (7,0),
        (8,0),
        (8,1),
        (8,2),
        (6,4),
        (6,5),
        (8,5),
        (0,5),
        (0,6),
        (0,1)

    ]
    wall_per = []
    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0], pos[1], wall)
        wall_per.append(wall)

    door_c = Door_closed()
    GAME_BOARD.register(door_c)
    GAME_BOARD.set_el(8, 8, door_c) 

    nic_positions = [
        (1,8),
        (3,0),
        (7,4),
        (3,5)
    ]

    nic_cg = []
    for pos in nic_positions:
        nic_c = NicC()
        GAME_BOARD.register(nic_c)
        GAME_BOARD.set_el(pos[0], pos[1], nic_c)
        nic_cg.append(nic_c)

    keanu_positions = [
        (0,4),
        (7,0),
        (7,7)
    ]

    keanus = []
    for pos in keanu_positions:
        kcr = Keanu()
        GAME_BOARD.register(kcr)
        GAME_BOARD.set_el(pos[0], pos[1], kcr)
        keanus.append(kcr)

    cat_positions = [
        (0,3),
        (4,3),
        (7,8)
    ]

    grumpy = []
    for pos in cat_positions:
        grumpy_cat = Grumpy()
        GAME_BOARD.register(grumpy_cat)
        GAME_BOARD.set_el(pos[0], pos[1], grumpy_cat)
        grumpy.append(grumpy_cat)

    GAME_BOARD.draw_msg("The object of this game is to find the One-True-God. Collect 3 of 'Him' to unlock the door.")
def keyboard_handler():
    direction = None

    if KEYBOARD[key.UP]:
        direction = "up"
        GAME_BOARD.draw_msg("Hint: Some of the stones can be moved... but be careful! You don't want to squish 'Him.'")
    if KEYBOARD[key.DOWN]:
        direction = "down"
        GAME_BOARD.draw_msg("Hint: Some of the stones can be moved... but be careful! You don't want to squish 'Him.'")
    if KEYBOARD[key.LEFT]:
        direction = "left"
        GAME_BOARD.draw_msg("Hint: Some of the stones can be moved... but be careful! You don't want to squish 'Him.'")
    if KEYBOARD[key.RIGHT]:
        direction = "right"
        GAME_BOARD.draw_msg("Hint: Some of the stones can be moved... but be careful! You don't want to squish 'Him.'")

    if direction:
        next_location = PLAYER.next_pos(direction)
        next_x = next_location[0]
        next_y = next_location[1]

        if -1 < next_x < 9 and -1 < next_y < 9:

            existing_el = GAME_BOARD.get_el(next_x, next_y)

            if existing_el:
                existing_el.interact(PLAYER)

            if existing_el is None or not existing_el.SOLID:
            # If there's nothing there_or_ if the existing element, is not solid, walk through
                GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
                GAME_BOARD.set_el(next_x, next_y, PLAYER)
    
