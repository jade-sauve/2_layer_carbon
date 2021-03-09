"""
Jade Sauve
Mary Margaret Stoll

March 2021

Final project for Climate Dynamics
presented to Kyle Armour and Gerard Roe

Ocean 2-layer model

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

directory_out_fig = ''

# model constants
rho = 1025 # density of sea water kg/m3
cw = 3985 # specific heat of sea water J/Kg/C
secondsperyear = 30.25*24*60*60*12

# parameters
gamma = 0.7 # ocean heat uptake efficiency parameter (W/m2/K), strength of coupling between layers
lambda0 = -1.2 #r adiative feedback parameter (W/m2/K)
e = 1.3 # ocean heat uptake efficacy (unitless)

hsfc = 100 # upper ocean depth, meters
hdeep = 1000 # deep ocean depth, meters 
# R = 4 #forcing for CO2 doubling, (W/m2)

### uses R from kyle_model - UPDATE

num_years = 300 # length of run in years

###################

# coefficients
csfc = rho * cw * hsfc # upper ocean, units J/m2/C
cdeep = rho * cw * hdeep # deep ocean, units J/m2/C

# define time variable
years = np.arange(num_years)

# define dataframe to hold Tsfc and Tdeep
df = pd.DataFrame(index=years,columns=['Tsfc','Tdeep'])

# this assumes that the initial temperature anomalies for the surface ocean and the deep ocean are 0C
for i in np.arange(0,num_years-1):

	df.loc[i+1,'Tsfc'] = df.loc[i,'Tsfc'] + ((lambda0 * df.loc[i,'Tsfc'] + R[i] + gamma*e*(df.loc[i,'Tdeep'] - df.loc[i,'Tsfc']))/csfc * secondsperyear)
	df.loc[i+1,'Tdeep'] = df.loc[i,'Tdeep'] + ((gamma * (df.loc[i,'Tsfc'] - df.loc[i,'Tdeep']))/ cdeep * secondsperyear)

toa_imbalance = R + lambda0*df['Tsfc'] - (e-1)*gamma*(df['Tsfc'] - df['Tdeep']) # top of atmosphere radiative imbalance
 
 

title = ''

plt.figure()
plt.plot(years, df['Tsfc'], label='Surface Layer')
plt.plot(years, df['Tdeep'],label='Deep Ocean Layer')
plt.xlabel('Years', size = 'xx-large')
plt.ylabel('Temperature Anomaly (K)', size = 'xx-large')
plt.legend(legend)
plt.title(title)
file_out = ''
# plt.savefig(directory_out_fig + file_out,format='eps',dpi=200)
plt.show()


title = ''

plt.figure()
plt.plot(df['Tsfc'], toa_imbalance)
plt.xlabel('Temperature Anomaly (K)', size = 'xx-large')
plt.ylabel('TOA imbalance (W/m2/K)', size = 'xx-large')
plt.title(title)
file_out = ''
# plt.savefig(directory_out_fig + file_out,format='eps',dpi=200)
plt.show()
















