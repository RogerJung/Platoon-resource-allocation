import pandas as pd
import numpy as np
import random
import argparse

parser = argparse.ArgumentParser(description='Code for generating data')
parser.add_argument("-t","--type", help="Input \'member\' or \'leader\'.")
args = parser.parse_args()

time = 2000
density = 200

l_or_m = args.type

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
    DF = pd.DataFrame(data)
else:
    mem_data = [[0 for x in range(density)] for y in range(time)] 
    data = pd.read_csv(f"leader_density{density}.csv", header=None)
    # data shape: (density, time)
    for i in range(density):
        for j in range(time):
            # print(i,j)
            rand = np.random.random()
            # # the probability different between from leader and member
            if rand < 0.1:
                if data[i][j] == 0:
                    mem_data[j][i] = 1
                else:
                    mem_data[j][i] = 0
            else:
                mem_data[j][i] = data[i][j]
    DF = pd.DataFrame(mem_data)

# save the dataframe as a csv file
DF.to_csv(f"{l_or_m}_density{density}.csv", index=False, header=False)