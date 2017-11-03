""" Window constants"""
SPRITE_SIZE = 30
NB_SPRITES = 15
WINDOW_SIDE = SPRITE_SIZE * NB_SPRITES
WINDOW_TITLE = "McGyver Maze"
WINDOW_TITLE_IN_GAME = "McGyver Maze | *PLAYING*"
INV_WIDTH = WINDOW_SIDE // 4
INV_HEIGHT = WINDOW_SIDE // 8

INV_ROW_SPACE = INV_WIDTH // SPRITE_SIZE
INV_COL_SPACE = INV_HEIGHT // SPRITE_SIZE

""" Sprites constants """
ICON_IMG = "../resources/img/macgyver.png"
MENU_IMG = "../resources/img/menu.png"
CONTROLS_IMG = "../resources/img/controls.png"
WALL_IMG = "../resources/img/wall_tile.png"
FLOOR_IMG = "../resources/img/floor_tile.png"

ITEMS_SPRITES = {
    "ether": "../resources/img/ether.png",
    "needle": "../resources/img/needle.png",
    "tube": "../resources/img/tube.png",
}

DECORS = {
    "wall": "../resources/img/wall_tile.png",
    "floor": "../resources/img/floor_tile.png",
}


""" Playable characters constants """
HEROES = {
    "mcgyver": "../resources/img/macgyver.png"
}


""" NPCS constants """
NPCS = {
    "guardian": ("G", "../resources/img/guardian.png")
}


""" Maps constants """
MAP = "../resources/map/map1.txt"
WALLS_MAP_NAME = "m"
FLOOR_MAP_NAME = "f"
ITEMS_MAP_NAME = "item"
