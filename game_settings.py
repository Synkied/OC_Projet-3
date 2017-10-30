""" Window constants"""
SPRITE_SIZE = 30
NB_SPRITES = 15
WINDOW_SIDE = SPRITE_SIZE * NB_SPRITES
WINDOW_TITLE = "McGyver Maze"
WINDOW_TITLE_IN_GAME = "McGyver Maze | *PLAYING*"
INV_WIDTH = WINDOW_SIDE // 2
INV_HEIGHT = WINDOW_SIDE // 4


""" Sprites constants """
ICON_IMG = "resources/img/macgyver.png"
MENU_IMG = "resources/img/menu.png"
CONTROLS_IMG = "resources/img/controls.png"
WALL_IMG = "resources/img/wall_tile.png"
FLOOR_IMG = "resources/img/floor_tile.png"

ITEMS_SPRITES = {
    "Ether": "resources/img/ether.png",
    "Needle": "resources/img/needle.png",
    "Tube": "resources/img/tube.png",
}


""" Playable characters constants """
HERO_CHAR = "resources/img/macgyver.png"


""" NPCS constants """
NPCS_DIC = {
    "GUARDIAN_CHAR": ("G", "resources/img/guardian.png")
}


""" Maps constants """
MAP = "map1.txt"
WALLS_MAP_NAME = "m"
FLOOR_MAP_NAME = "f"
ITEM_MAP_NAME = "i"
