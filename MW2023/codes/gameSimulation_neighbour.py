from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from itertools import product
import time

from myStrategicGames import MyAnnoyingNeighbourGame

def strategy_cooperative(h1, h2):
    """
        function representing the pure cooperative strategy 

    Args:
        h1 (list): list containing the full history of the game of the player playing the strategy represented by
            this function
        h2 (list): list containing the full history of the other player

    Returns:
        string: representation of the action/strategy which shall be applied
    """

    return 'q'

def strategy_nonCooperative(h1, h2):
    """
        function representing the pure non cooperative strategy 

    Args:
        h1 (list): full history of player playing the strategy represented by this function
        h2 (list): full history of the other player

    Returns:
        string: representation of the action which shall be applied
    """
    return 'l'

def strategy_titForTat(h1, h2):

    retVal = ''
    if len(h1) == 0:
        retVal = 'q'
    else:
        retVal = h2[-1]

    return retVal


def simulateGame(s1, s2, numDraws = 1000):

    history_1 = []
    history_2 = []

    cumPayoff_1 = 0.0
    cumPayoff_2 = 0.0

    for _ in range(0, numDraws):

        a1 = s1(history_1, history_2)
        a2 = s2(history_1, history_2)

        history_1.append(a1)
        history_2.append(a2)

        payoff = game.getPayoff(a1, a2)

        cumPayoff_1 += payoff[0]
        cumPayoff_2 += payoff[1]
    
    return cumPayoff_1, cumPayoff_2

def runEvolutionaryCompetition(strategyDict):
    numPopulationsPerStrategy = 100
    numGenerations = 5

    strategyKeys = list(strategyDict.keys())

    numStrategies = len(strategyDict)
    totNumPopulations = numStrategies * numPopulationsPerStrategy

    popRatesMtrx = np.zeros((numGenerations, numStrategies))
    popRatesMtrx[0, :] = (1 / numStrategies) * np.ones(numStrategies)

    s = 0.5 * totNumPopulations * (totNumPopulations + 1)

    for i in range(0, numGenerations):
        print('generation number {:d}:'.format(i))

        strategyPool = []
        popRates_prev = popRatesMtrx[i, :]

        # ### create population according to rates
        for j in range(0, numStrategies - 1):
            strategyPool += [(strategyKeys[j], strategyDict[strategyKeys[j]]) for l in range(0, int(popRates_prev[j] * totNumPopulations))]
        strategyPool += [(strategyKeys[-1], strategyDict[strategyKeys[-1]]) for l in range(len(strategyPool), totNumPopulations)]

        # ### evaluate strategies by means of tournament
        print('# ### start running tournament')
        start = time.time()
        scoreboard = runTournament(strategyPool)
        end = time.time()
        print('# ### end running tournament after {:.2f} secs'.format(end - start))

        # ### update population rates according to the result of the tournament - not needed in final round
        if i < numGenerations - 1:
            popRates = np.zeros(numStrategies)
            for j in range(0, numStrategies):
                popRates[j] = sum(scoreboard.loc[scoreboard['name'] == strategyKeys[j]]['rank'].tolist()) / s
            popRatesMtrx[i + 1, :] = popRates

    return popRatesMtrx

def runTournament(strategyPool):
    """
        this function is used to compare strategies with each other. for this purpose each strategy meets other
        strategy (including itself) over a predefinednumber of draws. the cumulative payoffs are used to evaluate
        the strategies.

    Args:
        strategyPool (list): list of pairs. the first element of the pair is a string giving the name of the strategy, 
            the second element is the strategy itself represented by means of a function)

    Returns:
        DataFrame: pandas dataframe representing the sorted (by cumulative payoffs) scoreboard of the tournament
    """
    # ### initialisations
    
    numStrategies = len(strategyPool)
    scoreList = [0.0 for _ in range(0, numStrategies)]
    
    strategyIdxList = np.arange(0, len(strategyPool), dtype = int)
    tournamentTable = [elem for elem in product(strategyIdxList, strategyIdxList)]

    numDraws = 1000

    # ### run tournament
    for elem in tournamentTable:

        cumPayoff_1, cumPayoff_2 = simulateGame(strategyPool[elem[0]][1], strategyPool[elem[1]][1], numDraws)

        scoreList[elem[0]] += cumPayoff_1
        scoreList[elem[1]] += cumPayoff_2

    # ### create scoreboard
    scoreboard = pd.DataFrame(list(zip([elem[0] for elem in strategyPool], scoreList)), columns = ['name', 'score'])
    scoreboard_sorted = scoreboard.sort_values(by = ['score'])
    scoreboard_sorted.insert(2, 'rank', np.arange(1, numStrategies + 1))

    return scoreboard_sorted

def plotResultsOfCompetition(dataDf, popRatesMtrx):

    # ### initialisations
    numGenerations = popRatesMtrx.shape[0]
    numStrategies = popRatesMtrx.shape[1]
    
    labelList = dataDf['name'].tolist()

    # ### create plots
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('generation vs. population rate')
    for j in range(0, numStrategies):
        ax.plot(np.arange(0, numGenerations, dtype = int), popRatesMtrx[:, j], label = labelList[j])

    ax.legend()
    plt.show()


if __name__ == '__main__':

    game = MyAnnoyingNeighbourGame()

    # create dataframe containing the strategies and corresponding informations - including color and linestyle for the
    # visualisation of the results. 
    dataDict = {
        's_1': ['coop', strategy_cooperative, 'b', '-'],
        's_2': ['nonCoop', strategy_nonCooperative, 'g', '-'], 
        's_3': ['titForTat', strategy_titForTat, 'y', '-']
    }
    strategyDataDf = pd.DataFrame.from_dict(dataDict, orient = 'index', columns = ['name', 'func', 'color', 'linestyle'])

    # run competition
    strategyDict = {}
    for elem in zip(strategyDataDf['name'].tolist(), strategyDataDf['func'].tolist()):
        strategyDict[elem[0]] = elem[1]

    popRatesMtrx = runEvolutionaryCompetition(strategyDict)
    
    plotResultsOfCompetition(strategyDataDf, popRatesMtrx)
