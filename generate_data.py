import pandas as pd
import numpy as np
import random
import argparse

parser = argparse.ArgumentParser(description='Code for generating data')
parser.add_argument("--dtype", help="Input \'member\' or \'leader\'.")
args = parser.parse_args()

time = 2000
density = 200

l_or_m = args.dtype

if l_or_m == 'leader':
    data = np.zeros((time, density), dtype=int)
    for i in range(time):
        for j in range(density):
            rand = np.random.random()
            if i == 0:
                if rand < 0.5:
                    data[i][j] = 1
                else:
                    data[i][j] = 0
            else:
                if rand < 0.9:
                    data[i][j] = data[i-1][j]
                elif rand > 0.9 and rand < 0.95:
                    data[i][j] = 0
                else:
                    data[i][j] = 1
else:
    data = pd.read_csv(f"leader_density{density}.csv", header=None)
    # data shape: (density, time)
    for i in range(density):
        for j in range(time):
            # print(i,j)
            rand = np.random.random()
            if rand < 0.15:
                if data[i][j] == 0:
                    data[i][j] = 1
                else:
                    data[i][j] = 0
        
DF = pd.DataFrame(data)
# save the dataframe as a csv file
DF.to_csv(f"{l_or_m}_density{density}.csv", index=False, header=False)