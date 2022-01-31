import pyglet
import math
from pyglet.window import key
window = pyglet.window.Window(32*5,32*5,fullscreen=False)

# notice: the renderer does this map correctly,
# but internally, you must access it by flipping the rows.
# this can be accomplished with the flipped_map.

map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]
flipped_map = map[::-1]

# idk why topy has to be like this..
# the renderer breaks unless this config is used.
# topx *should be set to len(map)*32 too, but,
# nobody cares because it isn't used internally
topx, topy = window.get_size()[0], len(map)*32
centerx, centery = topx // 2 , topy // 2

# this might be extended for a interactable objects update
class entity:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
player = entity(1, 1, "assets/player.png")

TileTextureSize = 32
TileTextureSize = int(TileTextureSize)

def get_image(tile_num):
    if tile_num == 0: return "assets/tile_normal.png"
    if tile_num == 1: return "assets/tile_wall.png"
    if tile_num == 2: return "assets/tile_flower_normal.png"
    if tile_num == 3: return "assets/tile_grass_normal.png"


def draw_relative(x, y, img, entity):
    temp = pyglet.image.load(img)
    # height, width = TileTextureSize, TileTextureSize
    # temp.scale =  min(temp.height, height)/max(temp.height, height), min(width, temp.width)/max(width, temp.width)
    # temp.scale_x, temp.scale_y = min(temp.height, height)/max(temp.height, height), max(min(width, temp.width), max(width, temp.width))
    temp.blit(x - (entity.x * TileTextureSize) + (TileTextureSize * 2), y - (entity.y * TileTextureSize) + (TileTextureSize * 2))

def draw_map(map):
    cx = 0
    cy = topy - TileTextureSize
    for Row in map:
        for Tile in Row:
            draw_relative(cx, cy, get_image(Tile), player)
            cx += TileTextureSize
        cy -= TileTextureSize
        cx = 0

def draw_entity(entity, relativeto):
    draw_relative(entity.x * TileTextureSize, entity.y * TileTextureSize, entity.image, relativeto)

def draw_player():
    temp = pyglet.resource.image(player.image)
    temp.blit(TileTextureSize * 2, TileTextureSize * 2)
def isWalkable(x,y):
    try:
        tile=flipped_map[y][x]
        if(tile in [1] or tile == None):
            return False
        return True
    except IndexError:
        return False

@window.event 
def on_draw():
    window.clear()
    draw_map(map)
    draw_player()

@window.event
def on_key_press(symb, mod):
    if(symb == key.W and isWalkable(player.x, player.y + 1) == True):
        player.y += 1
    if(symb == key.A and isWalkable(player.x - 1, player.y) == True):
        player.x -= 1
    if(symb == key.S and isWalkable(player.x, player.y - 1) == True):
        player.y -= 1
    if(symb == key.D and isWalkable(player.x + 1, player.y) == True):
        player.x += 1
    

pyglet.app.run()