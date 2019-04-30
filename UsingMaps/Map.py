import re
from Tile import Tile
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
        hit = False
        for row in self.Tiles:
            for col in row:
                if(col.hit):
                    if (col.x < player.x + 31 and
                        col.x + 31 > player.x and 
                        col.y < player.y + 31 and
                        col.y + 31 > player.y): 
                        ## switch to checking the move location and moving back based on each
                        ## two if statements to check current x and move y and then the second is move x and current y
                        col.Hit(player) ## move back
                        hit = True
                    if(hit):
                        break
            if(hit): ## this could break with multiple tiles
                break

    def Load(self):
        with open(self.mapfile, 'r') as f:
            newText = f.read()
            while '\n\n' in newText:
                newText = newText.replace('\n\n','\n')
            self.text = newText

        for m in re.findall(r"{([^}]*)}",self.text):
            loader = MapLoader(m)
            self.Tiles = loader.Load()

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
    
    def Load(self):
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
                if(i[:i.find("=")] == "hit"):
                    kdict[i[:i.find("=")]] = bool(i[i.find("=")+1:])
                if(i[:i.find("=")] == "color"):
                    kdict[i[:i.find("=")]] = tuple(list(map(int,re.sub(r"\(|\)","",i[i.find("=")+1:]).split(','))))
                if(i[:i.find("=")] == "sprite"):
                    kdict[i[:i.find("=")]] = i[i.find("=")+1:].replace('"', '')
                if(i[:i.find("=")] == "animate"):
                    kdict[i[:i.find("=")]] = bool(i[i.find("=")+1:])
            self.Key[k[:k.find(":")]] = kdict
        
        for k in self.Key:
            print(self.Key[k].get("hit",False))

    def LoadMap(self,text):
        rows = text.split(',')
        xpos = 0
        ypos = 0
        count = 0
        for r in rows:
            self.Tiles.append([])
            for c in r:
                self.Tiles[count].append(Tile(xpos,ypos,self.Key[c].get("color",(255,255,255)),self.Key[c].get("hit", False), self.Key[c].get("sprite", 0)))
                xpos += 32
            xpos = 0
            ypos += 32
            count += 1

# somemap = Map("Map.txt")

# somemap.Load()

