import matplotlib.pyplot as plt
import pandas as pd

df=pd.read_csv('data/simulation_data.csv')

field='trees'
plt.scatter([i for i in range(len(df[field]))],df[field])
plt.show()