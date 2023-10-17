# Prepare the data
sec_data = {
    'security': ['LA Municipal Bonds', 'Thompson Electronics', 'United Aerospace',
                 'Palmer Drugs', 'Nursing Homes'],
    'return': [5.3, 6.8, 4.9, 8.4, 11.8],
    }
CovM = {
    'LA Municipal Bonds':   [1.44,      -0.528,     -1.248,     -4.32,      -9.552],
    'Thompson Electronics': [-0.528,    19.36,      9.152,      5.28,       17.512],
    'United Aerospace':     [-1.248,    9.152,      27.04,      18.72,      10.348],
    'Palmer Drugs':         [-4.32,     5.28,       18.72,      144,        119.4],
    'Nursing Homes':        [-9.552,    17.512,     10.348,     119.4,      396.01]
    }
budget = 250000; beta = 0.1; simulation = 1000
# Prepare data frames
from pandas import DataFrame
df_sec = DataFrame(data=sec_data)
df_sec.set_index(['security'], inplace=True) #This line replace the default index
securities = df_sec.index
df_cov = DataFrame(data=CovM, index=securities, columns=securities)
# Choleski decomposition of the Covariance Matrix
import numpy as np
Cov_Matrix = df_cov.to_numpy()
L = np.linalg.cholesky(Cov_Matrix)
# Define the model
from pulp import *
prob = LpProblem('Portfolio_Risk_Management',LpMaximize)
# Define decision variables
investment = LpVariable.dicts('Invested_Value',securities,lowBound=0)
VaR = LpVariable('VaR')
Z = LpVariable.dicts('Shortfall',range(simulation),lowBound=0)
# Define the objective
prob += VaR - lpSum([Z[i] for i in range(simulation)])/beta/simulation, 'CVaR'
# Define the constraints
from numpy import random
prob += lpSum([investment[j] for j in securities]) <= budget
for i in range(simulation):
    r = L.dot(random.normal(0,1,len(securities))) + df_sec['return'].to_numpy()
    prob += Z[i] >= (
        VaR - lpSum([investment[securities[j]]*r[j] for j in range(len(securities))])/100)
prob.solve()
print('The CVaR =',value(prob.objective))
