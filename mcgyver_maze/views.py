import pygame
from game_settings import *
from exceptions import *


pygame.init()


# ===========================
#      Initialize pygame
# ===========================
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
    window.blit(images.guardian_img, guardian.case_position(lvl))
    window.blit(images.mcgyver_img, mcgyver.case_position(lvl))

    """
    For every item in the lvl's items,
    display each item if its attribute "displaying" is True.
    The item's image is seeked in the "images" Image class' instance.
    The item's position is seeked in this item
    Item class' instance @property "case_position"
    """
    for item in lvl.items:
        if lvl.items[item].displaying:
            window.blit(images.items[item], lvl.items[item].case_position)


def display_inventory(char, images, window):
    # creates new pygame Surface, with specified parameters
    inv = pygame.Surface((INV_WIDTH, INV_HEIGHT))
    # transparent surface
    inv.set_alpha(200)
    # black surface
    inv.fill((0, 0, 0))

    # defines inventory position on the screen
    # times 0.5 displays it in the middle of the window
    inv_x = (0.5 * WINDOW_SIDE) - (0.5 * INV_WIDTH)
    inv_y = (0.5 * WINDOW_SIDE) - (0.5 * INV_HEIGHT)

    # blit items in the inventory.
    # Inventory space is equal to INV_ROW_SPACE
    window.blit(inv, (inv_x, inv_y))
    for idx, item in enumerate(char.inventory._items):
        if idx < INV_ROW_SPACE:
            window.blit(images.items[item], (
                (idx + (NB_SPRITES - INV_ROW_SPACE) // 2) * SPRITE_SIZE, 7 * SPRITE_SIZE)
                # x's and y's coordinates of the blit
                # e.g.: x = 0 + (15 - 3) // 2 * 30 = 6 * 30 = 180
            )

        else:
            raise TooMuchItems("""Too many items to display.
            Number of items should be less or equal to: {}""".format(
                INV_ROW_SPACE * INV_COL_SPACE)
            )
