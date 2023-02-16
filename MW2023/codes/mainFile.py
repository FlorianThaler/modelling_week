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
import nashpy
from scipy.optimize import linprog

from gameAnalysisFunctions import checkIfNash_version_1
from gameAnalysisFunctions import checkIfNash_version_2
from gameAnalysisFunctions import findDominantStrategies

# define payoff matrices

n1 = 2      # number of actions of player 1
n2 = 2      # number of actions of player 2

A1 = np.zeros((n1, n2))
A2 = np.zeros((n1, n2))

        # payoff matrices for rock, paper, scissor, fountain
        # A1[0, 0] = 0
        # A1[0, 1] = -1
        # A1[0, 2] = 1
        # A1[0, 3] = -1

        # A1[1, 0] = 1
        # A1[1, 1] = 0
        # A1[1, 2] = -1
        # A1[1, 3] = 1

        # A1[2, 0] = -1
        # A1[2, 1] = 1
        # A1[2, 2] = 0
        # A1[2, 3] = -1

        # A1[3, 0] = 1
        # A1[3, 1] = -1
        # A1[3, 2] = 1
        # A1[3, 3] = 0

        # A2 = -A1

# payoff matrices for the prisoner's dilemma
A1[0, 0] = -1
A1[0, 1] = -15
A1[1, 0] = 0
A1[1, 1] = -10

A2[0, 0] = -1
A2[0, 1] = 0
A2[1, 0] = -15
A2[1, 1] = -10

# ### part I

print("# ### pure nash equilibria ###")
print("###############################")
print("")

# find all the nash equilibria - therefore iterate over
# all possible action pairs and check
for i in range(0, n1):
    for j in range(0, n2):
        # result = checkIfNash_version_1(A1, A2, i, j)
        result = checkIfNash_version_2(A1, A2, i, j)

        print("The strategy pair ({:d}, {:d}) forms a Nash equilibrium: {:s}".format(i, j, str(result)))


# ### part II

print("# ### mixed nash equilibria ###")
print("###############################")
print("")

# use the nashpy package to find also mixed nash equilibria
game = nashpy.Game(A1, A2)
nash_equilibria = game.support_enumeration()

print("All Nash equilibria (including mixed ones): ")
print(list(nash_equilibria))

# ### part III

print("# ### dominant strategies ###")
print("#############################")
print("")

# find all the dominant strategies of player 1 and player 2
dominant_strategies_pl_1, dominant_strategies_pl_2 = findDominantStrategies(A1, A2)
print("Dominant strategies for player 1: ")
print(dominant_strategies_pl_1)
print("Dominant strategies for player 2: ")
print(dominant_strategies_pl_2)

# ### part III

print("# ### maximin strategies ###")
print("############################")
print("")

c = [0, 0, -1]
A_eq = [[1, 1, 0]]
b_ub = [0, 0]
b_eq = [1]

x0_bounds = (0, None)
x1_bounds = (0, None)
x2_bounds = (None, None)

print(" > player 1:")

# adapt matrix A_ub - the only term which is player dependent for 
# finding a maximin strategy
A = np.ones((2, 3))
A[0 : n2, 0 : n1] = -A1.transpose()

A_ub = [A[0, :].tolist(), A[1, :].tolist()]
res = linprog(c, A_ub = A_ub, A_eq = A_eq, b_ub = b_ub, b_eq = b_eq, bounds = [x0_bounds, x1_bounds, x2_bounds])
print(res)

print(" > player 2:")

# find maximin strategies

A = np.ones((2, 3))
A[0 : n2, 0 : n1] = -A2.transpose()

A_ub = [A[0, :].tolist(), A[1, :].tolist()]
res = linprog(c, A_ub = A_ub, A_eq = A_eq, b_ub = b_ub, b_eq = b_eq, bounds = [x0_bounds, x1_bounds, x2_bounds])
print(res)