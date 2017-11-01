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

    def __init__(self, lvl_file, required_items):
        self.lvl_file = lvl_file
        self.items = {}
        self.generate()

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

    def generate(self):
        with open(self.lvl_file, "r") as lvl_file:
            """
            Nested list comprehension to build a 2D array,
            breaking down the specified lvl_file into rows and cols.
            """
            self.maze_map = [[sprite for sprite in line if sprite != "\n"] for line in lvl_file]

    def random_pos(self):
        """
        While self.maze_map[case_y][case_x] is not on a free space,
        search for a random position.
        Then set this random position to the ITEMS_MAP_NAME.
        This is to avoid items superposition.
        """
        case_x = 0
        case_y = 0
        while self.maze_map[case_y][case_x] != FLOOR_MAP_NAME:
            case_x = randint(1, (NB_SPRITES - 1))
            case_y = randint(1, (NB_SPRITES - 1))
        self.maze_map[case_y][case_x] = ITEMS_MAP_NAME
        return case_x, case_y


# ===========================
#      Items' class
# ===========================
class Item:
    """Describes an item"""

    def __init__(self, position):
        self.case_x = position[0]
        self.case_y = position[1]
        # turn to false when char position == item position
        self.show = True

    @property
    def case_position(self):
        """
        Case position of the item, to blit the image.
        Can be accessed via instance.case_position
        The case position is equal to the position of
        the item on the map's file times the SPRITE_SIZE.
        """
        return [self.case_x * SPRITE_SIZE, self.case_y * SPRITE_SIZE]


# ============================
#  Base class of all personas
# ============================
class GamePersona():
    """
    Base class for all objects (chars, items...) in the game
    """

    def __init__(self):
        self.case_x = 0
        self.case_y = 0
        self.x = self.case_x * SPRITE_SIZE
        self.y = self.case_y * SPRITE_SIZE

    def position(self, lvl):
        """
        Returns the position of the persona
        """
        return (self.x, self.y)


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
        self.case_x, self.case_y = self.random_npc_position(lvl)

    def random_npc_position(self, lvl):
        """
        Returns a random position for each instance of NPC
        """
        while lvl.maze_map[self.case_y][self.case_x] != NPCS[self.name][0]:
            self.case_x = randint(10, (NB_SPRITES - 1))
            self.case_y = randint(10, (NB_SPRITES - 1))
            if lvl.maze_map[self.case_y][self.case_x] in FLOOR_MAP_NAME:
                self.x = self.case_x * SPRITE_SIZE
                self.y = self.case_y * SPRITE_SIZE
                # set the case name as NPCS' initial
                lvl.maze_map[self.case_y][self.case_x] = NPCS[self.name][0]
        return self.x, self.y


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
        Collectable items are set in the ITEMS_SPRITES constant
        """
        for item in self.lvl.items:
            """
            For each item in the lvl's items,
            if item's case_x and case_y
            are equal to the char case_x and case_y,
            set the item's attribute "show" to False, to hide it
            """
            if self.lvl.items[item].case_x == self.case_x \
               and self.lvl.items[item].case_y == self.case_y \
               and self.lvl.items[item].show:
                self.inventory.add_object(item)
                self.lvl.items[item].show = False
                print(item.capitalize(), "collected")
        print(self.inventory._items)

    def check_inventory(self, window):
        """
        Checks the inventory for items present or not.
        Display the win or lose message accordingly
        Return bools to display in_menu or in_game
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

    def display_inventory(self, images, window):
        # creates new pygame Surface, with specified parameters
        inv = pygame.Surface((INV_WIDTH, INV_HEIGHT))
        # transparent surface
        inv.set_alpha(200)
        # black surface
        inv.fill((0, 0, 0))

        # defines inventory position on the screen
        inv_x = (0.5 * WINDOW_SIDE) - (0.5 * INV_WIDTH)
        inv_y = (0.5 * WINDOW_SIDE) - (0.5 * INV_HEIGHT)

        window.blit(inv, (inv_x, inv_y))
        for item in self.lvl.items:
            if item in self.inventory._items:
                if item == "ether":
                    ether = pygame.image.load(ITEMS_SPRITES["ether"])
                    window.blit(ether, (6 * SPRITE_SIZE, 7 * SPRITE_SIZE))
                if item == "needle":
                    needle = pygame.image.load(ITEMS_SPRITES["needle"])
                    window.blit(needle, (7 * SPRITE_SIZE, 7 * SPRITE_SIZE))
                if item == "tube":
                    tube = pygame.image.load(ITEMS_SPRITES["tube"])
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


# ===========================
#       Images' class
# ===========================
class Images:
    """
    Load images from different sources.
    DECORS for decors
    HEROES for playable chars
    NPCS for npcs
    and ITEMS_SPRITES for items
    """

    def __init__(self):
        self.wall_img = self.load_image(DECORS["wall"])
        self.floor_img = self.load_image(DECORS["floor"])
        self.mcgyver_img = self.load_image(HEROES["mcgyver"])
        self.guardian_img = self.load_image(NPCS["guardian"][1])
        self.decors = {}
        self.items = {}
        for item in ITEMS_SPRITES:
            try:
                self.items[item] = self.load_image(ITEMS_SPRITES[item])
            except KeyError as kerr:
                print("Image missing for {}. Original message: {}".format(item, kerr))
                exit()

        for decor in DECORS:
            try:
                self.decors[decor] = self.load_image(DECORS[decor])
            except KeyError as kerr:
                print("Image missing for {}. Original message: {}".format(decor, kerr))
                exit()

    @classmethod
    def load_image(cls, filename):
        """Calls pygame to load image and convert to transparent"""
        try:
            return pygame.image.load(filename).convert_alpha()
        except FileNotFoundError as fnferr:
            print("Image {} could not be opened. Here is the original message: {}".format(filename, fnferr))
            exit()


# ===============================================
#           Drawing elements on screen
# ===============================================
def draw_sprites(lvl, mcgyver, guardian, images, window):
    """
    This function is used to display every sprites on screen.
    """
    for line_idx, line in enumerate(lvl.maze_map):
        for sprite_idx, sprite in enumerate(line):
            # Used to set sprites' coords
            # compared to the fixed SPRITE_SIZE
            x = sprite_idx * SPRITE_SIZE
            y = line_idx * SPRITE_SIZE

            # Displays wall if sprite in maze_map
            # is in the WALLS_MAP_NAME constant(s)
            if sprite in WALLS_MAP_NAME:
                window.blit(images.wall_img, (x, y))

            # set the floor sprite where there is no wall
            if sprite not in WALLS_MAP_NAME:
                window.blit(images.floor_img, (x, y))

    # blit guardian and mcgyver (in this order)
    window.blit(images.guardian_img, guardian.position(lvl))
    window.blit(images.mcgyver_img, mcgyver.position(lvl))

    """
    For every item in the lvl's items,
    display each item if its attribute "show" is True.
    The item's image is seeked in the "images" Image class' instance.
    The item's position is seeked in this item
    Item class' instance @property "case_position"
    """
    for item in lvl.items:
        if lvl.items[item].show:
            window.blit(images.items[item], lvl.items[item].case_position)
