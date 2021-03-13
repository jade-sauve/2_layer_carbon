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

dir_in = '/Users/jadesauve/Coding/data/RCP/'
file_in = {'26':'R26_bulk.xls','45':'R45_bulk.xls','60':'R60_bulk.xls','85':'R85_bulk.xls'}

dir_out = '/Users/jadesauve/Coding/figures/'

# reservoir labels
res_dic = {0:'geology',1:'deep',2:'thermocline',3:'ml'}

ppmtoGtC = 2.12

F2x = 3.74 #forcing due to doubling CO2 (W/m2)
C0 = 280, # preindustrial CO2 concentration (ppm)
Fext = 0, # non-CO2 forcing (W/m2)

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
	'beta':0.7, # ocean heat uptake efficiency parameter (W/m2K), strength of coupling between layers
	'e':1.3, # ocean heat uptake efficacy (unitless)
}



###################

# open excel files and make df containing RCP emissions scenarios in ppm
for sce in file_in.keys():
	# open the file
	df = pd.read_excel (dir_in+file_in[sce])
	# select which row we want
	dfe = df[df['Variable'] == 'CO2 emissions - Total']
	dfw = dfe[df['Region'] == 'World']
	dfE = dfw[[2000,2005,2010,2020,2030,2040,2050,2060,2070,2080,2090,2100]]   # PgC/yr or GtC/yr
	# convert to ppm
	dfppm = dfE/ppmtoGtC
	dfppm = dfppm.transpose()
	dfppm = dfppm.rename(columns={16:sce})
	# concatenate all scenarios in one df
	try:
	    dfrcp = pd.concat([dfrcp, dfppm],axis=1)
	except NameError:
	    dfrcp = dfppm

# Make an emission pattern (one value per year) - will require dt=1 and C0 for 2000
dfEsce = pd.DataFrame(index=range(2000,2101),columns=dfrcp.columns)
for sce in file_in.keys():
	i=0
	for yr in dfrcp.index:
		try:
			# find the year where the emissions change
			yrend = dfrcp.index[i+1]
			dfEsce.loc[yr:yrend,sce] = dfrcp.loc[yr,sce]
		except IndexError:
			dfEsce.loc[yr:,sce] = dfrcp.loc[yr,sce]
		i=i+1



## section 3
# run full FAIR model
df, R = FAIR(attr_FAIR)

# run FAIR with alpha set to 1
df2, R2 = FAIR(attr_FAIR, set_alpha='off')

# plot
title = 'Temperature Anomaly in FAIR Model'
x = [df.index.values+1850, df.index.values+1850]
y1 = [df['T_sfc'], df['T_deep']]
y2 = [df2['T_sfc'], df2['T_deep']]
xlabel = 'Year'
ylabel = 'Temperature (K)'
label1 = ['FAIR','alpha=1']
label2 = ['T_sfc','T_deep']
colors = ['blue','red']
plot_1ax(x,y1,y2,xlabel,ylabel,label1,label2,title,colors,file_out=None)





## section 1
# run simple carbon model
# run with pulse
attr_KYLE['E'] = 200 #ppm
df3 = KYLE(attr_KYLE)

# run simple carbon model with time-varying E
attr_KYLE['E'] = 2 # ppm/yr
df4 = KYLE(attr_KYLE,E_time='on')

# run T model
# run a pulse in 2l-ocean model
dfpulse = twolmodel(attr_2lm)

# run time-varying in 2l model
attr_2lm['R'] = 0.02 # 4 W/m2 / 200 yr
dfnopulse = twolmodel(attr_2lm, pulse='off')

# run carbon model pulse in 2l model
# find forcing from [CO2]
F = F2x/np.log(2) * np.log(df3/C0) + Fext
# run
attr_2lm['R'] = F.values # 4 W/m2/300 yr
dftime = twolmodel(attr_2lm,pulse='time')

# run carbon model constant emissions in 2l model
F = F2x/np.log(2) * np.log(df4/C0) + Fext
attr_2lm['R'] = F.values # 4 W/m2/300 yr
dftime2 = twolmodel(attr_2lm,pulse='time')

# plot
title = 'Temperature Anomaly in 2-layer Ocean Model with Carbon Model Atmopsheric [CO2]'
x = [dftime.index.values+1850,dftime2.index.values+1850]
y1 = [dftime['T_sfc'],dftime2['T_sfc']]
y2 = [dftime['T_deep'],dftime2['T_deep']]
xlabel = 'Year'
ylabel = 'Temperature Anomaly (˚)'
label1 = ['T_sfc','T_deep']
label2 = ['Pulse','Constant Emissions']
colors = ['green','orange']
plot_1ax(x,y1,y2,xlabel,ylabel,label1,label2,title,colors,file_out=None)


title = 'Temperature Anomaly for Simple Scenarios in 2-layer Ocean Model'
x = [dfpulse.index.values+1850, dfnopulse.index.values+1850]
y1 = [dfpulse['T_sfc'],dfnopulse['T_sfc']]
y2 = [dfpulse['T_deep'],dfnopulse['T_deep']]
xlabel = 'Year'
ylabel = 'Temperature Anomaly (˚)'
label1 = ['T_sfc','T_deep']
label2 = ['Pulse','Constant Emissions']
colors = ['blue','red']
plot_1ax(x,y1,y2,xlabel,ylabel,label1,label2,title,colors,file_out=None)






# section 2
# run Fair on RCP scenarios
# requires different attributes due to the nature of the emission scenario
attr_FAIR['C0'] = 369.55 # ppm for the year 2000
attr_FAIR['dt'] = 1
attr_FAIR['endtime'] = 100

attr_FAIR['E'] =  dfEsce['26'].values # ppm/yr
df26, R26 = FAIR(attr_FAIR,E_time='on')

attr_FAIR['E'] =  dfEsce['45'].values # ppm/yr
df45, R45 = FAIR(attr_FAIR,E_time='on')

attr_FAIR['E'] =  dfEsce['60'].values # ppm/yr
df60, R60 = FAIR(attr_FAIR,E_time='on')

attr_FAIR['E'] =  dfEsce['85'].values # ppm/yr
df85, R85 = FAIR(attr_FAIR,E_time='on')

# plot
title = 'Temperature Anomaly for RCP Scenarios in FAIR'
x = [df26.index.values+2000, df45.index.values+2000,df60.index.values+2000,df85.index.values+2000]
y1 = [df26['T_sfc'],df45['T_sfc'],df60['T_sfc'],df85['T_sfc']]
y2 = [df26['T_deep'],df45['T_deep'],df60['T_deep'],df85['T_deep']]
xlabel = 'Year'
ylabel = 'Temperature Anomaly (˚)'
label1 = ['T_sfc','T_deep']
label2 = ['RCP2.6','RCP4.5','RCP6.0','RCP8.5']
colors = ['blue','red','green','orange']
plot_1ax(x,y1,y2,xlabel,ylabel,label1,label2,title,colors,file_out=None)





# plot the emissions scenarios for the method
title = 'Emissions Scenarios' # also mention the forcing scenarios: simple pulse and constant E
fig, ax = plt.subplots()
ax.plot(df3.index+1850, df3, linestyle='-', ms=4, color='blue',label='Pulse ')
ax.plot(df4.index+1850, df4, linestyle='-.', ms=4, color='blue',label='Constant Emissions')
ax.set_ylabel('Simple Carbon Model Atmopsheric Concentration (ppm)', color='blue')
plt.legend(loc='upper left')
ax2 = ax.twinx()
ax2.plot(dfEsce.index, dfEsce['26'], linestyle='-', ms=4, color='red',label='RCP2.6')
ax2.plot(dfEsce.index, dfEsce['45'], linestyle='-.', ms=4, color='red',label='RCP4.5')
ax2.plot(dfEsce.index, dfEsce['60'], linestyle='dotted', ms=4, color='red',label='RCP6.0')
ax2.plot(dfEsce.index, dfEsce['85'], linestyle='dashed', ms=4, color='red',label='RCP8.5')
ax2.set_ylabel('RCP Emissions (ppm/yr)', color='red')
ax.set_xlabel('Year')
ax.grid()
plt.title(title)
plt.legend(loc='upper right')
plt.show()









# extra plots
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

