"""
Jade Sauve
Mary Margaret Stoll

March 2021

Final project for Climate Dynamics
presented to Kyle Armour and Gerard Roe

Kyle's carbon model

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
CO2_PI = 280 # ppm
alpha = 0.5 # fraction taken up by the oceans
beta = 0.5
tau = 173 # years

# parameters
time = np.arange(0,300) # years

###################


## Kyle's model ##

# 1: Emissions - CO2 Concentration, pulse of CO2

E_CO2 = 200 #emissions of CO2 (in ppm)
CO2 = CO2_PI + alpha*E_CO2*(beta+(1-beta)*np.exp(-time/tau))

#Plot CO2 versus time
title = ''
plt.figure()
plt.plot(time,CO2)
plt.xlabel('Years')
plt.ylabel('CO2 Concentration (ppm)')
plt.grid()
plt.title(title)
file_out = ''
# plt.savefig(directory_out_fig + file_out,format='eps',dpi=200)
plt.show()


# 2: What about for time varying CO2 emissions?

E_CO2_time = 2 # ppm/year (constant)
CO2_timevarying = CO2_PI + alpha*E_CO2_time* (beta*time      + (1 - beta)*tau*(1 - np.exp(-time     /tau)))

#Plot CO2 versus time
title = ''
plt.figure()
plt.plot(time,CO2_timevarying)
plt.xlabel('Years')
plt.ylabel('CO2 Concentration (ppm)')
plt.title(title)
plt.grid()
file_out = ''
# plt.savefig(directory_out_fig + file_out,format='eps',dpi=200)
plt.show()


# 3: Turn concentration into radiative forcing
R = 5.35*np.log(CO2_timevarying/CO2_PI)

#Plot Radiative Forcing versus time
title = ''
plt.figure()
plt.plot(time,R)
plt.xlabel('Years')
plt.ylabel('Radiative Forcing (W/m2)')
plt.title(title)
plt.grid()
file_out = ''
# plt.savefig(directory_out_fig + file_out,format='eps',dpi=200)
plt.show()









