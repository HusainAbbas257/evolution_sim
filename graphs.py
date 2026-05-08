import matplotlib.pyplot as plt
import pandas as pd

df=pd.read_csv('data/simulation_data.csv')

for i in df.columns:
    field=i
    plt.scatter([i for i in range(len(df[field]))],df[field])
    plt.title(field)
    plt.show()