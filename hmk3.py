"""
hmk 3

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


dir_out = '/Users/jadesauve/Coding/figures/'


ppmtoGtC = 2.12

C0 = 280 # preindustrial CO2 concentration (ppm)

# use the attributes dictionaries below to select which parameters to pass to the models
attr_KYLE = {
# emissions parameters
	'E':200, # pulse CO2 emissions (ppm) or time varying (ppm/yr)
# time parameters
	'dt':1, # timestep size
	'endtime':300, # last year in the timesteps (yr)
# ocean model parameters
	'alpha':0.5, # fraction taken up by the oceans
	'beta':0.5,
	'tau':173 # years
}

attr_2lm = {
# emissions parameters
	'R':4, # forcing (W/m2)
# time parameters
	'dt':1, # time elapsed (years) - ex: 300 for a pulse, or 1 for a iterative process
	'endtime':300,
# ocean model parameters
	'hsfc':100, # upper ocean depth (meters)
	'hdeep':1000, # deep ocean depth (meters) 
	'lb':-1.2, # radiative feedback parameter (W/m2K)
	'beta':0.8, # ocean heat uptake efficiency parameter (W/m2K), strength of coupling between layers
	'e':1.3, # ocean heat uptake efficacy (unitless)
}



###################


# a)

attr_KYLE['E'] = 2
dfa = KYLE(attr_KYLE, E_time='on')

R = 3.7/np.log(2) * np.log(dfa['C']/280)
attr_2lm['R'] = R.values
dfa2 = twolmodel(attr_2lm, pulse='time')

Cacc = [0]
timesteps = np.arange(0,attr_2lm['endtime']+attr_2lm['dt'],attr_2lm['dt'])
for t in range(1,len(timesteps)):
	Cacc.append(Cacc[t-1] + 2)

title = 'Global Temperature vs Cumulative Emissions'
x = [Cacc]
y = [dfa2['T_sfc']]
xlabel = 'Cumulative Carbon Emissions (ppm)'
ylabel = 'Temperature Anomaly (˚C)'
label = ['']
colors = ['red']
file_out = dir_out+'hmk3_a'
plot_1var(x,y,xlabel,ylabel,label,title,colors,file_out=file_out)



# b)
# [Co2] before 200 yr
dfb = dfa.loc[0:200]
# [CO2] at 200yr
Ct0 = dfa.loc[200].values
t0=200
# concentration after that
t = np.arange(201,301)
C = Ct0 - (1-attr_KYLE['beta'])*(Ct0-C0)*(1-np.exp(-(t-t0)/attr_KYLE['tau']))
dfb = pd.concat([dfb, pd.DataFrame(index=t,columns=['C'],data=C)])

R = 3.7/np.log(2) * np.log(dfb['C']/280)
attr_2lm['R'] = R.values
dfb2 = twolmodel(attr_2lm, pulse='time')


title = 'Global Temperature for a Cessation of Emissions at t=200yr'
x = [dfb2.index]
y = [dfb2['T_sfc']]
xlabel = 'Time (years'
ylabel = 'Temperature Anomaly (˚C)'
label = ['']
colors = ['red']
file_out = dir_out+'hmk3_b'
plot_1var(x,y,xlabel,ylabel,label,title,colors,file_out=None)


# c)

attr_KYLE['tau'] = 10 # yr
dfc = KYLE(attr_KYLE, E_time='on')

R = 3.7/np.log(2) * np.log(dfc['C']/280)
attr_2lm['R'] = R.values
dfc2 = twolmodel(attr_2lm, pulse='time')

title = 'Global Temperature vs Cumulative Emissions'
x = [Cacc]
y = [dfc2['T_sfc']]
xlabel = 'Cumulative CH4 Emissions (ppm)'
ylabel = 'Temperature Anomaly (˚C)'
label = ['']
colors = ['red']
# file_out = dir_out+'hmk3_a'
plot_1var(x,y,xlabel,ylabel,label,title,colors)


# [Co2] before 200 yr
dfcc = dfc.loc[0:200]
# [CO2] at 200yr
Ct0 = dfc.loc[200].values
t0=200
# concentration after that
t = np.arange(201,301)
C = Ct0 - (1-attr_KYLE['beta'])*(Ct0-C0)*(1-np.exp(-(t-t0)/attr_KYLE['tau']))
dfcc = pd.concat([dfcc, pd.DataFrame(index=t,columns=['C'],data=C)])

R = 3.7/np.log(2) * np.log(dfcc['C']/280)
attr_2lm['R'] = R.values
dfcc2 = twolmodel(attr_2lm, pulse='time')


title = 'Global Temperature for a Cessation of Emissions at t=200yr'
x = [dfcc2.index]
y = [dfcc2['T_sfc']]
xlabel = 'Time (years'
ylabel = 'Temperature Anomaly (˚C)'
label = ['']
colors = ['blue']
# file_out = dir_out+'hmk3_b' 
plot_1var(x,y,xlabel,ylabel,label,title,colors,file_out=None)



# d)

attr_KYLE['tau'] = 173 #yr
attr_KYLE['beta'] = 0 

dfd = KYLE(attr_KYLE, E_time='on')

R = 3.7/np.log(2) * np.log(dfd['C']/280)
attr_2lm['R'] = R.values
dfd2 = twolmodel(attr_2lm, pulse='time')

title = 'Global Temperature vs Cumulative Emissions'
x = [Cacc]
y = [dfd2['T_sfc']]
xlabel = 'Cumulative CH4 Emissions (ppm)'
ylabel = 'Temperature Anomaly (˚C)'
label = ['']
colors = ['red']
# file_out = dir_out+'hmk3_a'
plot_1var(x,y,xlabel,ylabel,label,title,colors)


# [Co2] before 200 yr
dfdd = dfd.loc[0:200]
# [CO2] at 200yr
Ct0 = dfd.loc[200].values
t0=200
# concentration after that
t = np.arange(201,301)
C = Ct0 - (1-attr_KYLE['beta'])*(Ct0-C0)*(1-np.exp(-(t-t0)/attr_KYLE['tau']))
dfdd = pd.concat([dfdd, pd.DataFrame(index=t,columns=['C'],data=C)])

R = 3.7/np.log(2) * np.log(dfdd['C']/280)
attr_2lm['R'] = R.values
dfdd2 = twolmodel(attr_2lm, pulse='time')


title = 'Global Temperature for a Cessation of CH4 Emissions at t=200yr'
x = [dfdd2.index]
y = [dfdd2['T_sfc']]
xlabel = 'Time (years'
ylabel = 'Temperature Anomaly (˚C)'
label = ['']
colors = ['blue']
# file_out = dir_out+'hmk3_b' 
plot_1var(x,y,xlabel,ylabel,label,title,colors,file_out=None)




# e)
attr_KYLE['beta'] = 0.5

print(attr_KYLE)

dfe = KYLE(attr_KYLE, E_time='on')

R = 3.7*(dfe['C']**(1/2) - C0**(1/2)) / ((2*C0)**(1/2) - C0**(1/2)) 
# R = 3.7/np.log(2) * np.log(dfd['C']/280)
attr_2lm['R'] = R.values
dfe2 = twolmodel(attr_2lm, pulse='time')

title = 'Global Temperature vs Cumulative Emissions'
x = [Cacc]
y = [dfe2['T_sfc']]
xlabel = 'Cumulative CH4 Emissions (ppm)'
ylabel = 'Temperature Anomaly (˚C)'
label = ['']
colors = ['red']
# file_out = dir_out+'hmk3_a'
plot_1var(x,y,xlabel,ylabel,label,title,colors)




# [Co2] before 200 yr
dfee = dfe.loc[0:200]
# [CO2] at 200yr
Ct0 = dfe.loc[200].values
t0=200
# concentration after that
t = np.arange(201,301)
C = Ct0 - (1-attr_KYLE['beta'])*(Ct0-C0)*(1-np.exp(-(t-t0)/attr_KYLE['tau']))
dfee = pd.concat([dfee, pd.DataFrame(index=t,columns=['C'],data=C)])

R = 3.7*(dfee['C']**(1/2) - C0**(1/2)) / ((2*C0)**(1/2) - C0**(1/2)) 
# R = 3.7/np.log(2) * np.log(dfdd['C']/280)
attr_2lm['R'] = R.values
dfee2 = twolmodel(attr_2lm, pulse='time')


title = 'Global Temperature for a Cessation of CH4 Emissions at t=200yr'
x = [dfee2.index]
y = [dfee2['T_sfc']]
xlabel = 'Time (years'
ylabel = 'Temperature Anomaly (˚C)'
label = ['']
colors = ['blue']
# file_out = dir_out+'hmk3_b' 
plot_1var(x,y,xlabel,ylabel,label,title,colors,file_out=None)



# f)
"""
The main reason that global warming doesnt scale linearly with cumulative methane emissions is because 
methane does not remain in the atmopshere on long timescales like carbon (beta). The main reasons that tempertaure
does not remain constant after methane emissions cease is beause methane has a much shorter atmospheric lifetime
 than carbon (tau) and because methane does not remain in the atmosphere on long timescale (beta).

"""




