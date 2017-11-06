from random import randint
import pygame
from game_settings import *


# ===========================
#         Level class
# ===========================
class Level:
    """
    This is to generate the level's maze and items positions
    """

    def __init__(self, lvl_file, required_items):
        self.lvl_file = lvl_file
        self.items = {}
        self.generate_from_file()

        """
        For each item key in required_items,
        set each item in the items dict of the Level class
        by instanciating it with the Item class,
        taking in parameter the random_pos method of the Level class.
        This results in {"item_key": <xxx.Item object at *******>}.
        """
        for item in required_items.keys():
            self.items[item] = Item(self.random_pos())
        """
        Generates a 2D array to iterate on,
        to display the lvl in the display_lvl method.
        """

    def generate_from_file(self):
        with open(self.lvl_file, "r") as lvl_file:
            """
            Nested list comprehension to build a 2D array,
            breaking down the specified lvl_file into rows and cols.
            """
            self.maze_map = [
                [sprite for sprite in line if sprite != "\n"]
                for line in lvl_file
            ]

    def random_pos(self):
        """
        While self.maze_map[pos_y][pos_x] is not on a free space,
        search for a random position.
        Then set this random position to the ITEMS_MAP_NAME.
        This is to avoid items superposition.
        """
        pos_x = 0
        pos_y = 0
        while self.maze_map[pos_y][pos_x] != FLOOR_MAP_NAME:
            pos_x = randint(1, (NB_SPRITES - 1))
            pos_y = randint(1, (NB_SPRITES - 1))
        self.maze_map[pos_y][pos_x] = ITEMS_MAP_NAME
        return pos_x, pos_y


# ===========================
#        Items' class
# ===========================
class Item:
    """Describes an item"""

    def __init__(self, position):
        self.pos_x, self.pos_y = position
        # turn to false when char position == item position
        self.displaying = True

    @property
    def case_position(self):
        """
        Case position of the item, to blit the image.
        Can be accessed via instance.case_position
        The case position is equal to the position of
        the item on the map's file times the SPRITE_SIZE.
        """
        self.case_x = self.pos_x * SPRITE_SIZE
        self.case_y = self.pos_y * SPRITE_SIZE

        return (self.case_x, self.case_y)


# ============================
#  Base class of all personas
# ============================
class GamePersona():
    """
    Base class for all personas (Chars, NPC...) in the game
    """

    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.case_x = self.pos_x * SPRITE_SIZE
        self.case_y = self.pos_y * SPRITE_SIZE

    def case_position(self, lvl):
        """
        Returns the position of the persona
        """
        return (self.case_x, self.case_y)


# ===========================
#         NPCS' class
# ===========================
class NPC(GamePersona):
    """
    Class to create NPCS.
    """

    def __init__(self, lvl, name):
        self.name = name
        super().__init__()
        self.pos_x, self.pos_y = self.random_npc_position(lvl)

    def random_npc_position(self, lvl):
        """
        Returns a random position for each instance of NPC
        """
        while lvl.maze_map[self.pos_y][self.pos_x] != FLOOR_MAP_NAME:
            self.pos_x = randint(10, (NB_SPRITES - 1))
            self.pos_y = randint(10, (NB_SPRITES - 1))
        self.case_x = self.pos_x * SPRITE_SIZE
        self.case_y = self.pos_y * SPRITE_SIZE
        # set the case name as NPCS' initial
        lvl.maze_map[self.pos_y][self.pos_x] = NPCS[self.name][0]
        return self.case_x, self.case_y


# ===========================
#     Characters' class
# ===========================
class Character(GamePersona):
    """
    Class to create playable characters.
    """

    def __init__(self, lvl):
        self.lvl = lvl
        self.inventory = Inventory()
        super().__init__()

    def move(self, direction):
        """
        Defines the movement of the hero.
        Gets the direction specified in type(str),
        and gets the hero on the case if it's not a wall.
        """
        if direction == "right":
            # to not get out of the screen
            # NB_SPRITES - 1:
            # because there are 15 sprites,
            # but we start counting from 0
            # so it's 0 to 14 (15 sprites)
            if self.pos_x < (NB_SPRITES - 1):
                # check if the case is not a wall
                if self.lvl.maze_map[self.pos_y][self.pos_x + 1] \
                   not in WALLS_MAP_NAME:
                    # if it is not, go by one case
                    self.pos_x += 1
                    # move the hero sprite on the case
                    self.case_x = self.pos_x * SPRITE_SIZE
                    self.collect_item()

        if direction == "left":
            if self.pos_x > 0:
                if self.lvl.maze_map[self.pos_y][self.pos_x - 1] \
                   not in WALLS_MAP_NAME:
                    self.pos_x -= 1
                    self.case_x = self.pos_x * SPRITE_SIZE
                    self.collect_item()

        if direction == "up":
            if self.pos_y > 0:
                if self.lvl.maze_map[self.pos_y - 1][self.pos_x] \
                   not in WALLS_MAP_NAME:
                    self.pos_y -= 1
                    self.case_y = self.pos_y * SPRITE_SIZE
                    self.collect_item()

        if direction == "down":
            if self.pos_y < (NB_SPRITES - 1):
                if self.lvl.maze_map[self.pos_y + 1][self.pos_x] \
                   not in WALLS_MAP_NAME:
                    self.pos_y += 1
                    self.case_y = self.pos_y * SPRITE_SIZE
                    self.collect_item()

    def collect_item(self):
        """
        Collects the items from the map.
        Collectable items are set in the ITEMS_SPRITES constant
        """
        for item in self.lvl.items:
            """
            For each item in the lvl's items,
            if item's pos_x and pos_y
            are equal to the char pos_x and pos_y,
            set the item's attribute "displaying" to False, to hide it
            """
            if (self.lvl.items[item].pos_x == self.pos_x and
                    self.lvl.items[item].pos_y == self.pos_y and
                    self.lvl.items[item].displaying):

                self.inventory.add_object(item)
                self.lvl.items[item].displaying = False
                print(item.capitalize(), "collected")
                print("Inventory:", self.inventory._items)

    def check_inventory(self, window):
        """
        Checks the inventory for items present or not.
        Display the win or lose message accordingly
        Return bools to display in_menu or in_game
        """
        myfont = pygame.font.Font(None, 60)
        if sorted(self.inventory._items) == sorted(ITEMS_SPRITES):
            # prints to the screen "YOU WIN"
            win_txt = myfont.render("YOU WIN!", 1, (0, 255, 0))
            window.blit(win_txt, (0.25 * WINDOW_SIDE, 0.45 * WINDOW_SIDE))
            pygame.display.flip()  # refreshes the screen to display msg
            pygame.time.delay(1500)  # wait 1.5s while displaying msg
            return False, True  # set in_game to False and in_menu to True

        elif sorted(self.inventory._items) != sorted(ITEMS_SPRITES):
            # prints to the screen "YOU LOSE"
            lose_txt = myfont.render("YOU LOSE!", 1, (255, 0, 0))
            window.blit(lose_txt, (0.25 * WINDOW_SIDE, 0.45 * WINDOW_SIDE))
            pygame.display.flip()  # refreshes the screen to display msg
            pygame.time.delay(1500)  # wait 1.5s while displaying msg
            return False, True  # set in_game to False and in_menu to True

        return True, False


# ===========================
#      Inventory's class
# ===========================
class Inventory:
    """
    Creates an Inventory object.
    It has an _items list used to store items.
    This object is iterable.
    """

    def __init__(self):
        self._items = []

    def __iter__(self):
        for item in self._items:
            yield item

    def add_object(self, item):
        # adds an item to the _items list
        self._items.append(item)


# ===========================
#       Images' class
# ===========================
class Images:
    """
    Load images from different sources.
    DECORS for decors
    HEROES for playable chars
    NPCS for npcs
    ITEMS_SPRITES for items
    """

    def __init__(self):
        self.wall_img = self.load_image(DECORS["wall"])
        self.floor_img = self.load_image(DECORS["floor"])
        self.mcgyver_img = self.load_image(HEROES["mcgyver"])
        self.guardian_img = self.load_image(NPCS["guardian"][1])
        self.items = {}
        for item in ITEMS_SPRITES:
            try:
                self.items[item] = self.load_image(ITEMS_SPRITES[item])
            except KeyError as kerr:
                print("Image missing for {}. \
                   Original message: {}".format(item, kerr))
                exit()

    def load_image(self, filename):
        """
        Calls pygame to load image for the given filename
        and convert alpha zones in transparent
        """
        try:
            return pygame.image.load(filename).convert_alpha()
        except FileNotFoundError as fnferr:
            print("Image {} could not be opened. \
               Here is the original message: {}".format(filename, fnferr))
            exit()
