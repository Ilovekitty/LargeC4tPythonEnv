from Tile import Tile
class QuestTile(Tile):
    def __init__(self, pos):
        super(QuestTile,self).__init__(pos)
        self.hasbeenhit = False
        self.questId = 0
        self.start = False
    
    def Hit(self, player):
        if(not self.hasbeenhit):
            if(self.start):
                player.quests.append(["movementquest", self.questId,self.time])
            else:
                removeQuest = []
                for i in player.quests:
                    if(i[1] == self.questId):
                        removeQuest.append(i)
                        player.done = True
                for i in removeQuest:
                    player.quests.remove(i)

            self.hasbeenhit = True
        return False
        
    def ResetHit(self):
        self.hasbeenhit = False
        return True
    
    def UpdateLoad(self, attr, value):
        ## our updates for this specific tile type
        if(attr == "time"):
            self.time = value
        if(attr == "id"):
            self.QuestId = value
        if(attr == "start"):
            self.start = value
        ## if we dont do any of those attributes
        super(QuestTile,self).UpdateLoad(attr,value)
