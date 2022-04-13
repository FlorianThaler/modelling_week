from scipy.optimize import linprog

c = [0, 0, 1]

A_ub = [[0, 2, -1], [1, 0, -1]]
A_eq = [[1, 1, 0]]

b_ub = [0, 0]
b_eq = [1]

x0_bounds = (0, None)
x1_bounds = (0, None)
x2_bounds = (None, None)

res = linprog(c, A_ub = A_ub, A_eq = A_eq, b_ub = b_ub, b_eq = b_eq, bounds = [x0_bounds, x1_bounds, x2_bounds])

print(res)

