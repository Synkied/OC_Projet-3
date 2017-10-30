from random import shuffle, randrange, randint
import pygame
from game_settings import *


# ===========================
#         Level class
# ===========================
class Level:
    """
    This is to generate and display the level's maze
    """

    def __init__(self, lvl_file):
        self.lvl_file = lvl_file
        """
        Generates a 2D array to iterate on,
        to display the lvl in the display_lvl method.
        """
        with open(self.lvl_file, "r") as lvl_file:
            """
            Nested list comprehension to build a 2D array,
            breaking down the specified lvl_file into rows and cols.
            """
            self.maze_map = [[sprite for sprite in line if sprite != "\n"] for line in lvl_file]

    def display_lvl(self, window):
        """
        Displaying the lvl sprites, in the specified window.
        """
        wall_sprite = pygame.image.load(WALL_IMG).convert()
        floor_sprite = pygame.image.load(FLOOR_IMG).convert()

        for line_idx, line in enumerate(self.maze_map):
            for sprite_idx, sprite in enumerate(line):
                # used to set sprites' coords
                # compared to the fixed sprite size
                x = sprite_idx * SPRITE_SIZE
                y = line_idx * SPRITE_SIZE

                # displays wall if sprite in maze_map
                # is equal to any of the items
                # in the WALLS_MAP_NAME constant
                if sprite in WALLS_MAP_NAME:
                    window.blit(wall_sprite, (x, y))

                # set the floor sprite where there is no wall
                if sprite not in WALLS_MAP_NAME:
                    window.blit(floor_sprite, (x, y))


# ===========================
#  Base class of all objects
# ===========================
class GameObj():
    """
    Base class for all objects (chars, items...) in the game
    """

    def __init__(self, img):
        self.img = pygame.image.load(img).convert_alpha()
        self.case_x = 0
        self.case_y = 0
        self.x = 0
        self.y = 0
        self.displaying = True

    def display(self, window):
        """
        Displays the object in the given window
        """
        # blits object to the screen,
        # using the instance's specified img and coords
        if self.displaying:
            window.blit(self.img, (self.x, self.y))

    def position(self, lvl):
        """
        Returns the position of the object
        (NPC, char, item...)
        """
        return lvl.maze_map[self.case_y][self.case_x]

    def _show_inventory(self, window):
        """
        Displays the inventory of the given char in the given window
        """
        Inventory.display_inventory(self, window)


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
        super().__init__(img=NPCS_DIC[self.name][1])
        self.random_npc_position(lvl)

    def random_npc_position(self, lvl):
        while lvl.maze_map[self.case_y][self.case_x] != NPCS_DIC[self.name][0]:
            # randomize position not too close to playable chars
            self.case_x = randint(10, 14)
            self.case_y = randint(10, 14)

            # Checks if a random map case is = to FLOOR_MAP_NAME
            # if it is, sets the item to this case
            # and sets the NPC initial as the case name
            if lvl.maze_map[self.case_y][self.case_x] in FLOOR_MAP_NAME:
                self.x = self.case_x * SPRITE_SIZE
                self.y = self.case_y * SPRITE_SIZE
                # set the case name as NPCS' initial
                lvl.maze_map[self.case_y][self.case_x] = NPCS_DIC[self.name][0]
                return


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
        super().__init__(img=HERO_CHAR)

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
        for key, value in ITEMS_SPRITES.items():
            # if the sprite that the hero is on is = to one of the keys...
            if self.lvl.maze_map[self.case_y][self.case_x] == key:
                # ... and if the key's value is not in the inventory already...
                if value not in self.inventory:
                    # ... add the key's associated value to the inventory
                    self.inventory.add_object(ITEMS_SPRITES[key])
                    print(ITEMS_SPRITES[key][0], "collected")
                    # set the sprite to a floor sprite (not working)
                    self.lvl.maze_map[self.case_y][self.case_x] = FLOOR_MAP_NAME  # not working atm


# ===========================
#         Items' class
# ===========================
class CollectableItems(GameObj):

    def __init__(self, item_const_key, lvl):
        self.item_const_key = item_const_key
        super().__init__(img=ITEMS_SPRITES[self.item_const_key][1])
        self.random_item_position(lvl)

    def random_item_position(self, lvl):
        # While the lvl map's case name at instance position
        # has not been updated with the key of the item,
        # search for a random position.
        # This is to avoid items superposition
        while lvl.maze_map[self.case_y][self.case_x] != self.item_const_key:
            # randomize position
            self.case_x = randint(1, 14)
            self.case_y = randint(1, 14)

            # Checks if a map case is = to FLOOR_MAP_NAME
            # if it is, sets the item to this case
            # and sets the item's item_const_key as the case name
            if lvl.maze_map[self.case_y][self.case_x] in FLOOR_MAP_NAME:
                self.x = self.case_x * SPRITE_SIZE
                self.y = self.case_y * SPRITE_SIZE
                # set the case name as item_const_key
                lvl.maze_map[self.case_y][self.case_x] = self.item_const_key
                return

        # # debugging
        # with open("txt.txt", "w") as test:
        #     test.write(str(lvl.maze_map))


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

    def display_inventory(self, window):
        # creates new pygame Surface, with specified parameters
        inv = pygame.Surface((INV_WIDTH, INV_HEIGHT))
        # transparent surface
        inv.set_alpha(200)
        # black surface
        inv.fill((0, 0, 0))

        # ++++++++++++++++++++++++++++
        #          Needs work
        # ++++++++++++++++++++++++++++
        # #todo: wrong item positioning in inventory
        window.blit(inv, ((0.5 * WINDOW_SIDE) - (0.5 * INV_WIDTH), (0.5 * WINDOW_SIDE) - (0.5 * INV_HEIGHT)))
        for item_idx, item in enumerate(self.inventory._items):
            item_img = pygame.image.load(self.inventory._items[item_idx][1])
            if item in self.inventory._items:
                if len(self.inventory._items) == 1:
                    window.blit(item_img, (7 * SPRITE_SIZE, 7 * SPRITE_SIZE))
                else:
                    window.blit(item_img, (8 * SPRITE_SIZE, 7 * SPRITE_SIZE))
