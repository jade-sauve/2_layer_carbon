"""
Jade Sauve
Mary Margaret Stoll

March 2021

Final project for Climate Dynamics
presented to Kyle Armour and Gerard Roe

FAIR model

"""

## Import packages ##
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy import optimize
import os
import sys
pht = os.path.abspath('/Users/jadesauve/Documents/Python/scripts/2_layer_carbon/')
if pht not in sys.path:
    sys.path.append(pht)
from modules import *


#### Parameters ####

directory_out_fig = '/Users/jadesauve/Coding/figures/'

# model constants from Millar et al 2017
a = (0.2173, 0.2240, 0.2824, 0.2763) # fraction of carbon emissions entering the reservoir 
tau = (1e6, 394.4, 36.54, 4.304) # decay time constant for the pool (yr)
r0 = 32.40 # preindustrial iIRF100 (yr)
rc = 0.019 # Increase in iIRF100 with cumulative carbon uptake (year/GtC)
rt = 4.165 # Increase in iIRF100 with warming (year/K)

rho = 1025 # density of sea water kg/m3
cw = 3985 # specific heat of sea water J/KgK
F2x = 3.74 #forcing due to doubling CO2 (W/m2)

yeartosec = 30.25*24*60*60*12
ppmtoGtC = 2.12

# parameters
E = 2 # annual CO2 emissions (ppm/yr)
Fext = 0 # non-CO2 forcing (W/m2)

dt = 0.1 # timestep size
endtime = 300 # last year in the timesteps (yr)

beta = 0.7 # ocean heat uptake efficiency parameter (W/m2K), strength of coupling between layers
lb = -1.2 # radiative feedback parameter (W/m2K)
e = 1.3 # ocean heat uptake efficacy (unitless)

hsfc = 100 # upper ocean depth, meters
hdeep = 1000 # deep ocean depth, meters 

set_alpha = 'off' # on or off

# initial conditions
C0 = 280 # preindustrial CO2 concentration (ppm)
alpha0 = 0.11 # preindustrial alpha from Millard et al

# reservoir labels
res_dic = {0:'geology',1:'deep',2:'thermocline',3:'ml'}

###################


# define model timesteps in years
timesteps = np.arange(0,endtime+dt,dt) 

# make a dataframe to hold the reservoir concentration anomaly with time (ppm)
R = pd.DataFrame(index=timesteps, columns=[0,1,2,3], data = np.zeros((len(timesteps), 4)))
# make a df to hold the atm. [CO2], the radiative forcing, the temperature anomalies and the scaling factor
df = pd.DataFrame(index = timesteps, columns=['T_sfc','T_deep','C','F','alpha'], data = np.zeros((len(timesteps), 5)))

# set initial conditions for atm. [CO2] (ppm) and alpha
df.iloc[0]['C'] = C0
df.iloc[0]['alpha'] = alpha0
if set_alpha is 'off':
        alpha = 1
        df['alpha'] = alpha

# run the model
for t in range(len(timesteps)-1):

	if set_alpha is 'on':
		# step 1: find IRF100 from previous T,C
		# accumulated carbon 
		Cacc = (E*timesteps[t] - (df.iloc[t]['C'] - C0))*ppmtoGtC # GtC
		
		LHS = r0 + rc*Cacc + rt*df.iloc[t]['T_sfc'] # yr

		# step 2: find alpha 
		# define the function for IRF100 that depends on alpha
		def IRF100(alpha):
			RHS = 0
			for i in range(0,4):
				RHS = RHS + alpha*a[i]*tau[i]*(1-np.exp(-100/(alpha*tau[i]))) # yr

			return RHS - LHS

		# use fsolve to find the roots
		alpha = fsolve(IRF100, df.iloc[t]['alpha']) 
		df.iloc[t+1,df.columns.get_indexer(['alpha'])] = alpha

	# step 3: update carbon pools concentration (ppm)
	for i in range(0,4):
		R.iloc[t+1,i] = R.iloc[t,i] + dt*(a[i]*E - R.iloc[t,i]/(alpha*tau[i]))

	# step 4: update atmopsheric [CO2] (ppm)
	df.iloc[t+1,df.columns.get_indexer(['C'])] = C0 + np.sum(R.iloc[t+1])

	# Update total radiative forcing (W/m2)
	F = F2x/np.log(2) * np.log(df.iloc[t+1]['C']/C0) + Fext
	df.iloc[t+1,df.columns.get_indexer(['F'])] = F

	# step 5: update global mean T anomaly
	df.iloc[t+1,df.columns.get_indexer(['T_sfc'])] = df.iloc[t]['T_sfc'] + (dt*yeartosec/(rho*cw*hsfc)) * (lb*df.iloc[t]['T_sfc'] + F + beta*e*(df.iloc[t]['T_deep'] - df.iloc[t]['T_sfc'])) 
	df.iloc[t+1,df.columns.get_indexer(['T_deep'])] = df.iloc[t]['T_deep'] + (dt*yeartosec/(rho*cw*hdeep)) * (beta * (df.iloc[t]['T_sfc'] - df.iloc[t]['T_deep'])) 


# plot the results
title = 'Carbon Pools Concentration Anomaly'
plt.figure()
for i in range(0,4):
	plt.plot(R.index,R[i],label=res_dic[i])
plt.legend()
plt.title(title)
plt.grid()
plt.xlabel('Time (yr)')
plt.ylabel('Concentration (ppm)')
file_out=''
# plt.savefig(directory_out_fig + file_out,format='eps',dpi=200)
plt.show()


title = 'Temperature Anomaly'
plt.figure()
plt.plot(df.index,df['T_sfc'],label='T_sfc')
plt.plot(df.index,df['T_deep'],label='T_deep')
plt.legend()
plt.title(title)
plt.grid()
plt.xlabel('Time (yr)')
plt.ylabel('Temperaturerature (K)')
file_out=''
# plt.savefig(directory_out_fig + file_out,format='eps',dpi=200)
plt.show()


title = 'Radiative Forcing and Atmospheric CO2 Concentration'
fig, ax = plt.subplots()
line1, = ax.plot(df.index, df['C'],label='[CO2]',color='blue') 
ax.set_ylabel('[CO2] (ppm)', color='blue')
ax2 = ax.twinx()
line2, = ax2.plot(df.index, df['F'],label='F',color='red')
ax2.set_ylabel('F (W/m2)', color='red')
ax.set_xlabel('Time (yr)')
ax.grid()
plt.title(title)
file_out=''
# plt.savefig(directory_out_fig + file_out,format='eps',dpi=200)
plt.show()


title = 'Scaling Factor for the Carbon Cycle Feedback'
plt.figure()
plt.plot(df.index,df['alpha'])
plt.title(title)
plt.grid()
plt.xlabel('Time (yr)')
plt.ylabel('Alpha')
file_out=''
# plt.savefig(directory_out_fig + file_out,format='eps',dpi=200)
plt.show()


