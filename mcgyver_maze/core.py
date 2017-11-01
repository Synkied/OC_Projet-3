from random import randint
import pygame
from game_settings import *


# ===========================
#         Level class
# ===========================
class Level:
    """
    This is to generate and display the level's maze
    """

    def __init__(self, lvl_file, items):
        self.lvl_file = lvl_file
        self.items = {}
        self.generate()
        self.random_pos()
        for item in items:
            self.items[item] = Item(self.random_pos())
        """
        Generates a 2D array to iterate on,
        to display the lvl in the display_lvl method.
        """

    def generate(self):
        with open(self.lvl_file, "r") as lvl_file:
            """
            Nested list comprehension to build a 2D array,
            breaking down the specified lvl_file into rows and cols.
            """
            self.maze_map = [[sprite for sprite in line if sprite != "\n"] for line in lvl_file]

    def random_pos(self):
        """
        # While the lvl map's case name at instance position
        # has not been updated with ITEM_MAP_NAME,
        # search for a random position.
        # This is to avoid items superposition
        """
        # randomize position
        case_x = 0
        case_y = 0
        while self.maze_map[case_y][case_x] != FLOOR_MAP_NAME:
            case_x = randint(0, (NB_SPRITES - 1))
            case_y = randint(0, (NB_SPRITES - 1))
        for item in self.items:
            self.maze_map[case_y][case_x] = "*"
        return (case_x, case_y)


# ===========================
#  Base class of all objects
# ===========================
class GameObj():
    """
    Base class for all objects (chars, items...) in the game
    """

    def __init__(self):
        # self.img = pygame.image.load(img).convert_alpha()
        self.case_x = 0
        self.case_y = 0
        self.x = 0
        self.y = 0


    def position(self, lvl):
        """
        Returns the position of the object
        (NPC, char, item...)
        """
        return (self.x, self.y)

    def _show_inventory(self, window):
        """
        Displays the inventory of the given char in the given window
        """
        self.display_inventory(window)


# ===========================
#         NPCS' class
# ===========================
class NPC(GameObj):
    """
    Class to create NPCS.
    """

    def __init__(self, lvl, name):
        self.name = name
        # Sets the image of the NPC,
        # according to its name
        super().__init__()
        self.case_x, self.case_y = self.random_npc_position(lvl)

    def random_npc_position(self, lvl):
        while lvl.maze_map[self.case_y][self.case_x] != NPCS[self.name][0]:
            self.case_x = randint(10, (NB_SPRITES - 1))
            self.case_y = randint(10, (NB_SPRITES - 1))
            if lvl.maze_map[self.case_y][self.case_x] in FLOOR_MAP_NAME:
                self.x = self.case_x * SPRITE_SIZE
                self.y = self.case_y * SPRITE_SIZE
                # set the case name as NPCS' initial
                lvl.maze_map[self.case_y][self.case_x] = NPCS[self.name][0]
        return (self.x, self.y)


# ===========================
#     Characters' class
# ===========================
class Character(GameObj):
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
            if self.case_x < (NB_SPRITES - 1):
                # check if the case is not a wall
                if self.lvl.maze_map[self.case_y][self.case_x + 1] not in WALLS_MAP_NAME:
                    # if it is not, go by one case
                    self.case_x += 1
                    # move the hero sprite on the case
                    self.x = self.case_x * SPRITE_SIZE
                    self.collect_item()

        if direction == "left":
            if self.case_x > 0:
                if self.lvl.maze_map[self.case_y][self.case_x - 1] not in WALLS_MAP_NAME:
                    self.case_x -= 1
                    self.x = self.case_x * SPRITE_SIZE
                    self.collect_item()

        if direction == "up":
            if self.case_y > 0:
                if self.lvl.maze_map[self.case_y - 1][self.case_x] not in WALLS_MAP_NAME:
                    self.case_y -= 1
                    self.y = self.case_y * SPRITE_SIZE
                    self.collect_item()

        if direction == "down":
            if self.case_y < (NB_SPRITES - 1):
                if self.lvl.maze_map[self.case_y + 1][self.case_x] not in WALLS_MAP_NAME:
                    self.case_y += 1
                    self.y = self.case_y * SPRITE_SIZE
                    self.collect_item()

    def collect_item(self):
        """
        Collects the items from the map.
        Collectable items are set in the SPRITES constant
        """
        for item in self.lvl.items:
            if (self.lvl.items[item].case_x == self.case_x and
                    self.lvl.items[item].case_y == self.case_y and
                    self.lvl.items[item].show):
                self.inventory.add_object(item)
                self.lvl.items[item].show = False
                print(item, "collected")
        # print(self.inventory._items)

    def check_inventory(self, npc, window):
        """
        Checks the inventory of self against given NPC.
        """
        myfont = pygame.font.SysFont("monospace", 60)
        if sorted(self.inventory._items) == sorted(ITEMS_SPRITES):

            # prints to the screen "YOU WIN"
            win_txt = myfont.render("YOU WIN!", 1, (0, 255, 0))
            window.blit(win_txt, (80, 175))
            pygame.display.flip()
            pygame.time.delay(1500)
            return False, True

        elif sorted(self.inventory._items) != sorted(ITEMS_SPRITES):

            # prints to the screen "YOU LOSE"
            lose_txt = myfont.render("YOU LOSE!", 1, (255, 0, 0))
            window.blit(lose_txt, (80, 175))
            pygame.display.flip()
            pygame.time.delay(1500)
            return False, True

        return True, True

    def display_inventory(self, window):
        # creates new pygame Surface, with specified parameters
        inv = pygame.Surface((INV_WIDTH, INV_HEIGHT))
        # transparent surface
        inv.set_alpha(200)
        # black surface
        inv.fill((0, 0, 0))

        window.blit(inv, ((0.5 * WINDOW_SIDE) - (0.5 * INV_WIDTH), (0.5 * WINDOW_SIDE) - (0.5 * INV_HEIGHT)))
        for item in self.inventory._items:
            if item == "Ether":
                ether = pygame.image.load(ITEMS_SPRITES["Ether"])
                window.blit(ether, (6 * SPRITE_SIZE, 7 * SPRITE_SIZE))
            if item == "Needle":
                needle = pygame.image.load(ITEMS_SPRITES["Needle"])
                window.blit(needle, (7 * SPRITE_SIZE, 7 * SPRITE_SIZE))
            if item == "Tube":
                tube = pygame.image.load(ITEMS_SPRITES["Tube"])
                window.blit(tube, (8 * SPRITE_SIZE, 7 * SPRITE_SIZE))


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


class Images:
    """Load images from given config parameters"""

    def __init__(self):
        self.wall = self.load_image(DECORS["wall"])
        self.floor = self.load_image(DECORS["floor"])
        self.mcgyver = self.load_image(HEROES["mcgyver"])
        self.guardian = self.load_image(NPCS["guardian"])
        self.decors = {}
        self.items = {}
        for item in ITEMS_SPRITES:
            try:
                self.items[item] = self.load_image(ITEMS_SPRITES[item])
            except KeyError:
                print("Image missing for {}".format(decor))
                exit()

        for decor in DECORS:
            try:
                self.decors[decor] = self.load_image(DECORS[decor])
            except KeyError:
                print("Image missing for {}".format(decor))
                exit()

        for hero in DECORS:
            try:
                self.decors[decor] = self.load_image(DECORS[decor])
            except KeyError:
                print("Image missing for {}".format(decor))
                exit()

    @classmethod
    def load_image(cls, filename):
        """Calls pygame to load image and convert to transparent"""
        try:
            return pygame.image.load(filename).convert_alpha()
        except FileNotFoundError:
            print("Image {} could not be opened.".format(filename))
            exit()


class Item:
    """Describes an item"""

    def __init__(self, position):
        self.case_x = position[0]
        self.case_y = position[1]
        self.show = True

    @property
    def case_position(self):
        """Pixel position of the item, useful when bliting the image"""
        return [self.case_x * SPRITE_SIZE, self.case_y * SPRITE_SIZE]


def draw_sprites(lvl, mcgyver, guardian, images, window):

    for line_idx, line in enumerate(lvl.maze_map):
        for sprite_idx, sprite in enumerate(line):
            # used to set sprites' coords
            # compared to the fixed sprite size
            x = sprite_idx * SPRITE_SIZE
            y = line_idx * SPRITE_SIZE

            # displays wall if sprite in maze_map
            # is equal to any of the items
            # in the WALLS_MAP_NAME constant
            if sprite in WALLS_MAP_NAME:
                window.blit(images.wall, (x, y))

            # set the floor sprite where there is no wall
            if sprite not in WALLS_MAP_NAME:
                window.blit(images.floor, (x, y))

    window.blit(images.mcgyver, mcgyver.position(lvl))
    window.blit(images.guardian, guardian.position(lvl))

    for item in lvl.items:
        if lvl.items[item].show:
            window.blit(images.items[item], lvl.items[item].case_position)
