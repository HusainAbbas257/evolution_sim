from src import simulation
import pandas as pd

sim=simulation.Simulation()
data=sim.mainloop()      
# saving tocsv
df=pd.DataFrame(data)
df.to_csv('data/simulation_data.csv',index=False)
