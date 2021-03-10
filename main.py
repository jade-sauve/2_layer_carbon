"""
Jade Sauve
Mary Margaret Stoll

March 2021

Final project for Climate Dynamics
presented to Kyle Armour and Gerard Roe

see modules.py to find the models and the plot functions

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

# reservoir labels
res_dic = {0:'geology',1:'deep',2:'thermocline',3:'ml'}

# use the attributes dictionaries below to select which parameters to pass to the models

attr_FAIR = {
# emissions parameters
	'E':2, # annual CO2 emissions (ppm/yr)
	'Fext':0, # non-CO2 forcing (W/m2)
# time parameters
	'dt':0.1, # timestep size
	'endtime':300, # last year in the timesteps (yr)
# ocean model parameters
	'beta':0.7, # ocean heat uptake efficiency parameter (W/m2K), strength of coupling between layers
	'lb':-1.2, # radiative feedback parameter (W/m2K)
	'e':1.3, # ocean heat uptake efficacy (unitless)
	'hsfc':100, # upper ocean depth, meters
	'hdeep':1000, # deep ocean depth, meters 
# initial conditions
	'C0':280, # preindustrial CO2 concentration (ppm)
	'alpha0':0.11 # preindustrial alpha from Millard et al
}

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

###################

# run full model
df, R = FAIR(attr_FAIR)

# run with alpha set to 1
df2, R2 = FAIR(attr_FAIR, set_alpha='off')

# run simple model
attr_KYLE['E'] = 200 #ppm
df3 = KYLE(attr_KYLE)

# run simple model with time-varying E
attr_KYLE['E'] = 2 # ppm/yr
df4 = KYLE(attr_KYLE,E_time='on')



# plot 
title = 'Radiative Forcing and Atmospheric CO2 Concentration'
x = [df.index, df.index]
y1 = [df['C'], df2['C']]
y2 = [df['F'], df2['F']]
ls = ['-','-.']
xlabel = 'Time (yr)'
ylabel = ['[CO2] (ppm)','F (W/m2)',]
label1 = ['FAIR','alpha=1']
label2 = ['C','F']
colors = ['blue','red']
# file_out = dir_out+'F_C_compare'
plot_2ax(x,y1,y2,ls,xlabel,ylabel,label1,label2,title,colors,file_out=None)


title = 'Temperature Anomaly'
x = [df.index, df.index]
y1 = [df['T_sfc'], df['T_deep']]
y2 = [df2['T_sfc'], df2['T_deep']]
xlabel = 'Time (yr)'
ylabel = 'Temperature (K)'
label1 = ['FAIR','alpha=1']
label2 = ['T_sfc','T_deep']
colors = ['blue','red']
plot_1ax(x,y1,y2,xlabel,ylabel,label1,label2,title,colors,file_out=None)


title = 'Carbon Pools Concentration Anomaly'
x = [df.index, df.index,df.index,df.index]
y1 = [R[0],R[1],R[2],R[3]]
y2 = [R2[0],R2[1],R2[2],R2[3]]
xlabel = 'Time (yr)'
ylabel = 'Concentration (ppm)'
label1 = ['FAIR','alpha=1']
label2 = ['geologic processes','deep ocean','ocean thermocline','ocean ml']
colors = ['blue','red','green','orange']
plot_1ax(x,y1,y2,xlabel,ylabel,label1,label2,title,colors,file_out=None)


title = 'Atmopsheric CO2 Concentration in the Simple Model'
x = [df3.index, df4.index]
y1 = [df3['C']]
y2 = [df4['C']]
xlabel = 'Time (yr)'
ylabel = 'CO2 Concentration (ppm)'
label1 = ['Pulse','Time-varying']
label2 = ['']
colors = ['blue']
plot_1ax(x,y1,y2,xlabel,ylabel,label1,label2,title,colors,file_out=None)



# title = 'Atmopsheric CO2 Concentration in the Simple Model'
# plt.figure()
# plt.plot(df3.index,df3['C'])
# plt.xlabel('Years')
# plt.ylabel('CO2 Concentration (ppm)')
# plt.grid()
# plt.title(title)
# file_out = ''
# # plt.savefig(directory_out_fig + file_out,format='eps',dpi=200)
# plt.show()

# title = 'Atmopsheric CO2 Concentration in the Simple Model with Time-varying Emissions'
# plt.figure()
# plt.plot(df4.index,df4['C'])
# plt.xlabel('Years')
# plt.ylabel('CO2 Concentration (ppm)')
# plt.grid()
# plt.title(title)
# file_out = ''
# # plt.savefig(directory_out_fig + file_out,format='eps',dpi=200)
# plt.show()

# title = 'Atmopsheric CO2 Concentration in the Simple Model'
# x = [df3.index, df4.index]
# y1 = [df3['C']]
# y2 = [df4['C']]
# ls = ['-','-.']
# xlabel = 'Time (yr)'
# ylabel = ['Pulse (ppm)','Time-varying (ppm)']
# label1 = ['']
# label2 = ['Pulse','Time-varying']
# colors = ['blue','red']
# plot_2ax(x,y1,y2,ls,xlabel,ylabel,label1,label2,title,colors,file_out=None)

