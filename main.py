"""
Jade Sauve
Mary Margaret Stoll

March 2021

Final project for Climate Dynamics
presented to Kyle Armour and Gerard Roe

"""

## Import packages ##
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
pht = os.path.abspath('/Users/jadesauve/Documents/Python/scripts/2_layer_carbon/')
if pht not in sys.path:
    sys.path.append(pht)
from modules import *


#### Parameters ####

# model constants from Millar et al 2017
a = (0.2173, 0.2240, 0.2824, 0.2763) #fraction of carbon emissions entering the reservoir 
tau = (1e6, 394.4, 36.54, 4.304) # decay time constant for the pool 9(r)
r0 = # preindustrial iIRF100
rc = # Increase in iIRF100 with cumulative carbon uptake
rt = # Increase in iIRF100 with warming

# parameters
E = # annual CO2 emissions (ppm/yr)
dt = # timestep size
timesteps = # number of timestep

# initial conditions
C0 = # preindustrial CO2 concentration 
R = [0,0,0,0]

# reservoir labels
res_dic = {0:'geology',1:'deep',2:'thermocline',3:'ml'}

###################


# make a dataframe to hold the reservoir change with time
R = np.DataFrame(index=timesteps, columns=[0,1,2,3])
# make a df to hold the temperature anomaly with time
T = np.DataFrame(index = timesteps, columns=['T_sfc','T_deep'])



# FAIR

# find IRF100 from previous T,C
# atmopsheric [CO2]
C = C0 + sum(R.loc[t]) # where R is an array with shape = 4
# accumulated carbon
Cacc = E - (C-C0) # this is summed  over time.... check
# 
irf100 = r0 + rc*Cacc + rt*T.loc[t,'T_sfc']

# use fsolve to find the roots
def IRF100(alpha):
	RHS = 0
	for i in range(0,4):
		RHS = RHS + alpha*a[i]*tau[i]*(1-np.exp(-100/alpha*tau[i]))

	return RHS - irf100

alpha = fsolve(IRF100,alpha0)










