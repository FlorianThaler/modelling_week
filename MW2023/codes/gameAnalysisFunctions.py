"""
    authors: 
        Hannah Grabner
        Eileen Schmieger
        Elodie Korsatko
        Tabea Solhdju
        Laura König
        Sianna Zinterl
"""
import numpy as np


def checkIfNash_version_1(A1, A2, i, j):
    """
        given the payoff matrices for player 1, and player 2 this function
        checks if the strategy pair (i, j) is a Nash equilibrium

    Args:
        A1 (2d array): payoff matrix for player 1
        A2 (2d array): payoff matrix for player 2
        i (integer): index of strategy 
        j (integer): index of strategy

    Returns:
        boolean value indicating if (i, j) forms a Nash equilibrium
    """

    # determine number of actions or (strategies) player 1 and player 2
    # can apply
    numActions_pl_1, numActions_pl_2 = A1.shape

    # introduce auxiliary lists
    nash_test_list1 = [False for _ in range(0,numActions_pl_1)]
    nash_test_list2 = [False for _ in range(0,numActions_pl_2)]

    # use the payoff matrices to check if the strategy pair (i, j) is
    # a nash equilibrium
    # NOTE:
    #   > we use two for loops here since player 1 and player 2 may have
    #       different numbers of actions/strategies they can apply
    for k in range(0, numActions_pl_1):
        if A1[i, j] >= A1[k, j]:
            nash_test_list1[k] = True
    for k in range (0,numActions_pl_2):
        if A2[i, j] >= A2[i, k]:
            nash_test_list2[k] = True

    # (i, j) is a nash equilibrium if and only if all the above queries are true
    # this is checked next
    test1 = np.all(nash_test_list1)
    test2 = np.all(nash_test_list2)
    retVal = None
    if np.all([test1, test2]):
        retVal = True
    else:
        retVal = False

    return retVal

def checkIfNash_version_2(A1, A2, i, j):
    """
        given the payoff matrices for player 1, and player 2 this function
        checks if the strategy pair (i, j) is a Nash equilibrium

    Args:
        A1 (2d array): payoff matrix for player 1
        A2 (2d array): payoff matrix for player 2
        i (integer): index of strategy 
        j (integer): index of strategy
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    Returns:
        boolean value indicating if (i, j) forms a Nash equilibrium
    """
    # determine number of actions or (strategies) player 1 and player 2
    # can apply
    numActions_pl_1, numActions_pl_2 = A1.shape

    # auxiliary variables
    y1 = 1
    y2 = 1

    # use the payoff matrices to check if the strategy pair (i, j) is
    # a nash equilibrium
    for k in range(0, numActions_pl_1):
        if A1[i, j] >= A1[k, j]:
            y1 = y1 * 1
        else:
            y1 = y1 * 0
    for k in range (0,numActions_pl_2):
        if A2[i, j] >= A2[i, k]:
            y2 = y2 * 1
        else:
            y2 = y2 * 0
    
    retVal = None
    if y1 * y2 == 1:
        retVal = True
    else:
        retVal = False

    return retVal

def findDominantStrategies(A1, A2):
    """
    this function determines all the dominant strategies for player 1 and player 2

    Args:
        A1 (2d array): payoff matrix of player 1
        A2 (2d array): payoff matrix of player 2

    Returns:
        lists containing the dominant strategies for player 1 and player 2 respectively
    """
    numActions_pl_1, numActions_pl_2 = A1.shape

    dominant_strategies_list_pl_1 = []
    dominant_strategies_list_pl_2 = []
    # search for dominant strategies for player 1
    for i in range(0, numActions_pl_1):
        # check if strategy i is dominant
        y = 1
        for j in range(0, numActions_pl_2):
            for k in range(0, numActions_pl_1):
                if A1[i, j] >= A1[k, j]:
                    y = y * 1
                else:
                    y = y * 0
        if y == 1:
            dominant_strategies_list_pl_1.append(i)
    
    # search for dominant strategies for player 2
    for j in range(0, numActions_pl_2):
        # check if strategy j is dominant
        y = 1
        for i in range(0, numActions_pl_1):
            for k in range(0, numActions_pl_2):
                if A2[i, j] >= A2[j, k]:
                    y = y * 1
                else:
                    y = y * 0
        if y == 1:
            dominant_strategies_list_pl_2.append(j)

    return dominant_strategies_list_pl_1, dominant_strategies_list_pl_2