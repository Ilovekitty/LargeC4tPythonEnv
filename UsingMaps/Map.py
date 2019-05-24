import re
from Tile import Tile
from QuestTile import QuestTile
class Map(object):
    def __init__(self, filename):
        self.mapfile = filename
        self.worldx = 0
        self.worldy = 0
        self.tiles = []
        self.text = ""
        self.othertext = []
        self.Tiles = []

    def Update(self, dt):
        for row in self.Tiles:
            for col in row:
                if(len(col.sprite)):
                    col.Update(dt) 

    def CheckHit(self, player):
        hitx = False
        hity = False
        
        for row in self.Tiles:
            for col in row:
                hitTilex = False
                hitTiley = False
                if(col.hit):
                    if (col.x < player.nextx + 31 and
                        col.x + 31 > player.nextx and 
                        col.y < player.y + 31 and
                        col.y + 31 > player.y):
                        hitx = col.Hit(player)
                        hitTilex = True

                    if (col.x < player.x + 31 and
                        col.x + 31 > player.x and 
                        col.y < player.nexty + 31 and
                        col.y + 31 > player.nexty): 
                        hity = col.Hit(player)
                        hitTiley = True
                    
                    if(not hitTiley and not hitTilex):
                        col.ResetHit()
        
        if(not hitx):
            player.x = player.nextx
        else:
            player.nextx = player.x
        if(not hity):
            player.y = player.nexty
        else:
            player.nexty = player.y
        
                    

    def Load(self):
        with open(self.mapfile, 'r') as f:
            newText = f.read()
            while '\n\n' in newText:
                newText = newText.replace('\n\n','\n')
            self.text = newText

        for m in re.findall(r"{([^}]*)}",self.text):
            loader = MapLoader(m)
            self.Tiles = loader.Load(self.Tiles)

    def Render(self, surface, playerpos):
        self.worldx,self.worldy = playerpos
        for Row in self.Tiles:
            for T in Row:
                T.Render(surface,self.worldx,self.worldy)

class MapLoader(object):
    def __init__(self,MapText):
        self.mapText = MapText
        self.Key = {}
        self.Tiles = []
    
    def Load(self, Tiles):
        self.Tiles = Tiles
        loadingstate = 0
        text = ""
        fullmap = ""
        keytext = []
        for line in self.mapText.split('\n'):
            text = line.replace(' ','')
            if("type:" in line):
                ## load type data
                loadingstate = 1
            if("key:" in line):
                ## load key data
                loadingstate = 2
            if("map:" in line):
                ## load map data
                loadingstate = 3

            if(loadingstate == 1):
                ## set some variable so we know what type
                text[text.find(":")+1:].replace(',','')
            if(loadingstate == 2):
                keytext.append(text.replace("key:[","").replace("]]","]"))
            if(loadingstate == 3):
                fullmap += text.replace("map:[","").replace("]","")

        self.LoadKey(keytext)
        self.LoadMap(fullmap)

        return self.Tiles

            
            
    def LoadKey(self,keytext):
        for k in keytext:
            kdict = {}
            for i in re.sub(r"\[|\],?","",k[k.find(":")+1:]).split("|"):
                ## check for attributes and add them to a dictionary
                if(i[:i.find("=")] == "hit"
                    or i[:i.find("=")] == "animate"):
                    kdict[i[:i.find("=")]] = bool(i[i.find("=")+1:])
                if(i[:i.find("=")] == "color"):
                    kdict[i[:i.find("=")]] = tuple(list(map(int,re.sub(r"\(|\)","",i[i.find("=")+1:]).split(','))))
                if(i[:i.find("=")] == "type" 
                    or i[:i.find("=")] == "id" 
                    or i[:i.find("=")] == "sprite"):
                    kdict[i[:i.find("=")]] = i[i.find("=")+1:].replace('"', '')
                if(i[:i.find("=")] == "time"):
                    kdict[i[:i.find("=")]] = float(i[i.find("=")+1:].replace('"', ''))
                if(i[:i.find("=")] == "start" ):
                    kdict[i[:i.find("=")]] = int(i[i.find("=")+1:].replace('"', ''))
                    
            self.Key[k[:k.find(":")]] = kdict
        
        for k in self.Key:
            print(self.Key[k].get("hit",False))

    def LoadMap(self,text):
        rows = text.split(',')
        if(self.Tiles == []): 
            buildtiles = True 
        else: 
            buildtiles = False


        xsize = 32
        ysize = 32
        y = 0
        x = 0
        for r in rows:
            if(buildtiles):
                self.Tiles.append([])
            for c in r:
                if(buildtiles):
                    ## check type of Tile and default to base tile
                    if(self.Key[c].get("type", False)):
                        if(self.Key[c].get("type") == "Quest"):
                            self.Tiles[y].append(QuestTile((xsize*x,ysize*y)))
                    else:
                        self.Tiles[y].append(Tile((xsize*x,ysize*y)))
                ## Update the color of the tile
                if(self.Key[c].get("color", False)):
                    self.Tiles[y][x].UpdateLoad("color",self.Key[c]["color"])
                ## Updates time for tiles that need it
                if(self.Key[c].get("time", False)):
                    self.Tiles[y][x].UpdateLoad("time", self.Key[c]["time"])
                ## Gives an Id for Quests(or anything else that needs an id)
                if(self.Key[c].get("id", False)):
                    self.Tiles[y][x].UpdateLoad("id", self.Key[c]["id"])
                if(self.Key[c].get("start", False)):
                    self.Tiles[y][x].UpdateLoad("start",self.Key[c].get("start"))
                ## update the Hit detection
                if(self.Key[c].get("hit", False)):
                    self.Tiles[y][x].UpdateLoad("hit",self.Key[c].get("hit"))
                ## update the sprite
                if(self.Key[c].get("sprite", False)):
                    self.Tiles[y][x].UpdateLoad("sprite",self.Key[c].get("sprite"))
                x += 1
            x = 0
            y += 1

# somemap = Map("Map.txt")

# somemap.Load()

