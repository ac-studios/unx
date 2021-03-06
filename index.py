from numpy import isin
import pyglet
import math
from pyglet.window import key
window = pyglet.window.Window(32*5,32*5,fullscreen=False)

# notice: the renderer does this map correctly,
# but internally, you must access it by flipping the rows.
# this can be accomplished with the flipped_map.

# idk why topy has to be like this..
# the renderer breaks unless this config is used.
# topx *should be set to len(map)*32 too, but,
# nobody cares because it isn't used internally

# this might be extended for a interactable objects update
class Game:
    def __init__(self):
        self.maps = []
        self.index = 0
        self.map = []
        self.flipped_map = []
        self.entities = []
        self.uistate = "game"
    def loadmap(self, idx):
        if(idx >= len(self.maps)): return self.gameOver() # this prevents IndexErrors
        self.map = self.maps[idx].map
        self.flipped_map = self.map[::-1]
        self.entities = self.maps[idx].entities
        global topy
        topy = len(self.map)*32
        player.x = self.maps[idx].spawnx
        player.y = self.maps[idx].spawny
    def gameOver(self):
        self.uistate = "over"
    def incg(self):
        t=self.index+0
        self.index+=1
        return t
    def loadnextmap(self):
        self.loadmap(self.incg())
    def checkInteraction(self, x , y):
        for E in self.entities:
            if(E.x == x and E.y == y):
                try:
                    E.triggerOnInteract()
                finally:
                    pass
    def checkCover(self, x, y):
        for E in self.entities:
            if(E.x == x and E.y == y):
                try:
                    E.triggerOnCover()
                finally:
                    pass
    def getTile(self, x, y):
        return self.flipped_map[y][x]
    def drawEntities(self):
        for E in self.entities:
            draw_entity(E, player)
class Map:
    def __init__(self, mapraw, entities, spawnx, spawny):
        self.map = mapraw
        self.entities = entities
        self.spawnx = spawnx
        self.spawny = spawny

game = Game()

topx, topy = window.get_size()[0], len(game.map)*32
centerx, centery = topx // 2 , topy // 2

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
        self.facing = "up"

        # predef
        self.oncover = None
        self.oninteract = None
    def triggerOnCover(self):
        try:
            self.oncover()
        finally:
            pass
    def triggerOnInteract(self):
        try:
            self.oninteract()
        finally:
            pass
class int_door:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = "assets/int_door.png"
        self.collidable = False
        self.facing = "up"

        # predef
        self.oninteract = None
    def triggerOnCover(self):
        game.loadnextmap()
class int_coin:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.image = "assets/int_coin.png"
        self.collidable = False
        self.facing = "up"
        self.countable = True

        # predef
        self.oninteract = None
    def triggerOnCover(self):
        if(self.countable == True):
            player.coins += 1
            self.image = "assets/transparent_x32.png" # make us appear invisible
            self.countable = False
class Player:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.facing = "up"
        self.coins = 0

player = Player(1, 1, "assets/player.png")

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
    if tile_num == 4: return "assets/tile_crimson_wall.png"

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
        tile=game.getTile(x, y)
        if(tile in [1,4] or tile == None):
            return False
        return True
    except IndexError:
        return False

@window.event 
def on_draw():
    if(game.uistate == "game"):
        window.clear()
        draw_map(game.map)
        game.drawEntities()
        draw_player()
    elif(game.uistate == "over"):
        window.clear()
        coin_lbl = pyglet.text.Label(text="coins : " + str(player.coins))
        title_lbl = pyglet.text.Label(text="game over", y=32*2, x=32)
        coin_lbl.draw()
        title_lbl.draw()

@window.event
def on_key_press(symb, mod):
    if(game.uistate == "game"):
        if(symb == key.W and isWalkable(player.x, player.y + 1) == True):
            player.y += 1
            player.facing = "up"
            game.checkCover(player.x, player.y)
        if(symb == key.A and isWalkable(player.x - 1, player.y) == True):
            player.x -= 1
            player.facing = "left"
            game.checkCover(player.x, player.y)
        if(symb == key.S and isWalkable(player.x, player.y - 1) == True):
            player.y -= 1
            player.facing = "down"
            game.checkCover(player.x, player.y)
        if(symb == key.D and isWalkable(player.x + 1, player.y) == True):
            player.x += 1
            player.facing = "right"
            game.checkCover(player.x, player.y)
        if(symb == key.E):
            if(player.facing == "up"):
                game.checkInteraction(player.x, player.y + 1)
            if(player.facing == "left"):
                game.checkInteraction(player.x - 1, player.y)
            if(player.facing == "down"):
                game.checkInteraction(player.x, player.y - 1)
            if(player.facing == "right"):
                game.checkInteraction(player.x + 1, player.y)
game.maps = [Map([
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 2, 3, 4, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
], [
    int_door(4, 4)
], 1, 1), Map([
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
], [ 
    int_door(1, 8),
    int_coin(1, 1),
    int_coin(2, 1),
    int_coin(3, 1),
    int_coin(4, 1)
], 1, 1)]

game.loadnextmap()

pyglet.app.run()