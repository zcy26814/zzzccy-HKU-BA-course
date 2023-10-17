from scipy import optimize
import numpy as np
np.set_printoptions(suppress=True)

t = 250000

c = np.array([-1.1, 5.0, 1.7, 0.3, 7.5])

A = np.array([[-1, 0, 0, 0, 0], [0, 0, 0, -1, -1],
             [-0.8, 0, 0, 1, 0], [1, 1, 1, 1, 1]])

b = np.array([-0.2 * t, -0.4 * t, 0, t])

bounds = np.array([[0, t], [0, t], [0, t], [0, t], [0, t]])

res = optimize.linprog(c, A, b, method='highs', bounds=bounds)

print(res)