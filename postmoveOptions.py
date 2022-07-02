from enums import PostmoveOptionsEnums

class postmoveOptions:
    # TODO: make it so some units inherit this and can only wait
    def __init__(self):
        self.options = [PostmoveOptionsEnums.WAIT]
        self.attackableEnemies = []

    def getCurrentOptions(self):
        return self.options
    
    def hasAttackOption(self):
        return PostmoveOptionsEnums.ATTACK in self.options

    def appendOption(self, option):
        self.options.append(option)
    
    def resetOptions(self):
        self.options = [PostmoveOptionsEnums.WAIT]
        self.attackableEnemies = []

    def getAttackableEnemies(self):
        return self.attackableEnemies

    def setAttackableEnemies(self, attackableEnemies):
        self.attackableEnemies = attackableEnemies
    
    
    