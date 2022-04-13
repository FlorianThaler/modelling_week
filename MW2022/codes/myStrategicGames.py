class MyStrategicGame:
    """
        this class models a stratefic 2-player game with finite strategy sets. the payoffs of the game
        are represented by means of a table, which is implemented as dictionary, where:
            > actions of player 1 are listed rowwise
            > actions of player 2 are listed columnwise
    """

    def __init__(self, payoffDict):

        self.payoffDict = None
        self.setPayoffDict(payoffDict)

    def getPayoffDict(self):
        return self.payoffDict

    def setPayoffDict(self, payoffDict):
        self.payoffDict = {}

        for key1 in payoffDict.keys():  
            self.payoffDict[key1] = {}
            for key2 in payoffDict[key1]:
                self.payoffDict[key1][key2] = payoffDict[key1][key2]

    def getPayoff(self, s1, s2):
        return self.payoffDict[s1][s2]

    
class MyAnnoyingNeighbourGame(MyStrategicGame):

    def __init__(self):

        payOffDict = {}
        payOffDict['q'] = {}
        payOffDict['q']['q'] = (2, 2)
        payOffDict['q']['l'] = (-3, 3)

        payOffDict['l'] = {}
        payOffDict['l']['q'] = (3, -3)
        payOffDict['l']['l'] = (-2, -2)

        super(MyAnnoyingNeighbourGame, self).__init__(payOffDict)
