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
class Game:
    def __init__(self):
        self.maps = ["assets/map0.json", "assets/map1.json"]
        self.index = 0
        self.map = []
        self.flipped_map = []
        self.entities = []
    def loadmap(self, idx):
        # this will need to be updated for JSON.parse, fs, etc
        self.map = self.maps[idx]
        self.flipped_map = self.map[::-1]
    def incg(self):
        t=self.index+0
        self.index+=1
        return t
    def loadnextmap(self):
        self.loadmap(self.incg())
    def checkInteraction(self):
        pass
    def checkCover(self):
        pass

game = Game()
class entity:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.facing = "up"
class entity2:
    def __init__(self, x=0, y=0, image="", collidable=False):
        self.x = x
        self.y = y
        self.image = image
        self.collidable = collidable

        # predef
        self.oncover = None
        self.oninteract = None

        # push to game stack
        game.entities.append(self)
    def triggerOnCover(self):
        try:
            self.oncover()
        finally:
            pass
    def triggerOnInteract(self):
        try:
            self.oncover()
        finally:
            pass
player = entity(1, 1, "assets/player.png")

# the images are all 32x32. this is just 32
TileTextureSize = 32
TileTextureSize = int(TileTextureSize)

# essentially, we convert the numbers in the
# map, to actual images
def get_image(tile_num):
    if tile_num == 0: return "assets/tile_normal.png"
    if tile_num == 1: return "assets/tile_wall.png"
    if tile_num == 2: return "assets/tile_flower_normal.png"
    if tile_num == 3: return "assets/tile_grass_normal.png"

# we draw the image "relative" to the player,
# so it ensures the player is always "centered"
# on the screen
def draw_relative(x, y, img, entity):
    temp = pyglet.image.load(img)
    # fun math
    temp.blit(x - (entity.x * TileTextureSize) + (TileTextureSize * 2), y - (entity.y * TileTextureSize) + (TileTextureSize * 2))

# we cycle through each number in the map and draw it
def draw_map(map):
    cx = 0
    cy = topy - TileTextureSize
    for Row in map:
        for Tile in Row:
            draw_relative(cx, cy, get_image(Tile), player)
            cx += TileTextureSize
        cy -= TileTextureSize
        cx = 0

# this helps if we need to draw entites like chests sometime
def draw_entity(entity, relativeto):
    draw_relative(entity.x * TileTextureSize, entity.y * TileTextureSize, entity.image, relativeto)

# self explanatory
def draw_player():
    temp = pyglet.resource.image(player.image)
    temp.blit(TileTextureSize * 2, TileTextureSize * 2)

# we check if the x and y are walkable. 
# if its not, we return False
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
        player.facing = "up"
    if(symb == key.A and isWalkable(player.x - 1, player.y) == True):
        player.x -= 1
        player.facing = "left"
    if(symb == key.S and isWalkable(player.x, player.y - 1) == True):
        player.y -= 1
        player.facing = "down"
    if(symb == key.D and isWalkable(player.x + 1, player.y) == True):
        player.x += 1
        player.facing = "right"

pyglet.app.run()