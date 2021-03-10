"""
Jade Sauve
Mary Margaret Stoll

March 2021

Final project for Climate Dynamics
presented to Kyle Armour and Gerard Roe

Modules

"""

## Import packages ##
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy import optimize


## models

def KYLE(attr,E_time='off'):
    """
    This is the simple model presented in class
    To use a time-varying E, set E_time = 'on'

    """
    #### Parameters ####
    C0 = 280 # ppm
    
    ###################

    # define time steps of the model
    timesteps = np.arange(0,attr['endtime']+attr['dt'],attr['dt']) # years

    if E_time is 'off':
        CO2 = C0 + attr['alpha']*attr['E']*(attr['beta'] + (1 - attr['beta'])*np.exp(-timesteps/attr['tau']))
    elif E_time is 'on':
        CO2 = C0 + attr['alpha']*attr['E']*(attr['beta']*timesteps + (1 - attr['beta'])*attr['tau']*(1 - np.exp(-timesteps/attr['tau'])))

    # define a df to hold the data
    df = pd.DataFrame(index=timesteps,columns=['C'],data=CO2)

    return df




def FAIR(attr,set_alpha='on'):
    """
    This is the full FAIR model
    requires a constant emissions per year
    alpha can be 'on' or 'off'

    """

    #### Parameters ####
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

    # reservoir labels
    res_dic = {0:'geology',1:'deep',2:'thermocline',3:'ml'}

    ###################

    # define time steps of the model
    timesteps = np.arange(0,attr['endtime']+attr['dt'],attr['dt']) 

    # make a dataframe to hold the reservoir concentration anomaly with time (ppm)
    R = pd.DataFrame(index=timesteps, columns=res_dic.keys(), data = np.zeros((len(timesteps), 4)))
    # make a df to hold the atm. [CO2], the radiative forcing, the temperature anomalies and the scaling factor
    df = pd.DataFrame(index = timesteps, columns=['T_sfc','T_deep','C','F','alpha'], data = np.zeros((len(timesteps), 5)))

    # set initial conditions for atm. [CO2] (ppm) and alpha
    df.iloc[0]['C'] = attr['C0']
    df.iloc[0]['alpha'] = attr['alpha0']
    if set_alpha is 'off':
        alpha = 1
        df['alpha'] = alpha

    # run the model
    for t in range(len(timesteps)-1):

        if set_alpha is 'on':
            # step 1: find IRF100 from previous T,C
            # accumulated carbon 
            Cacc = (attr['E']*timesteps[t] - (df.iloc[t]['C'] - attr['C0']))*ppmtoGtC # GtC
            
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
            R.iloc[t+1,i] = R.iloc[t,i] + attr['dt']*(a[i]*attr['E'] - R.iloc[t,i]/(alpha*tau[i]))

        # step 4: update atmopsheric [CO2] (ppm)
        df.iloc[t+1,df.columns.get_indexer(['C'])] = attr['C0'] + np.sum(R.iloc[t+1])

        # Update total radiative forcing (W/m2)
        F = F2x/np.log(2) * np.log(df.iloc[t+1]['C']/attr['C0']) + attr['Fext']
        df.iloc[t+1,df.columns.get_indexer(['F'])] = F

        # step 5: update global mean T anomaly
        df.iloc[t+1,df.columns.get_indexer(['T_sfc'])] = df.iloc[t]['T_sfc'] + (attr['dt']*yeartosec/(rho*cw*attr['hsfc'])) * (attr['lb']*df.iloc[t]['T_sfc'] + F + attr['beta']*attr['e']*(df.iloc[t]['T_deep'] - df.iloc[t]['T_sfc'])) 
        df.iloc[t+1,df.columns.get_indexer(['T_deep'])] = df.iloc[t]['T_deep'] + (attr['dt']*yeartosec/(rho*cw*attr['hdeep'])) * (attr['beta'] * (df.iloc[t]['T_sfc'] - df.iloc[t]['T_deep'])) 

    return df, R




## Plot 


def plot_2ax(x,y1,y2,ls,xlabel,ylabel,label1,label2,title,colors,file_out=None):
    """
    Plot 2 or more variables on two different axis
    To save the figure, set file_out = '/directory/for/figures/file_name'

    """
    fig, ax = plt.subplots()
    for i in range(len(y1)):
        ax.plot(x[i], y1[i], linestyle=ls[i], ms=4, color=colors[0],label=label1[i]+', '+label2[0])
    ax.set_ylabel(ylabel[0], color=colors[0])

    ax2 = ax.twinx()
    for i in range(len(y2)):
        ax2.plot(x[i], y2[i], linestyle=ls[i], ms=4, color=colors[1],label=label1[i]+', '+label2[1])
    ax2.set_ylabel(ylabel[1], color=colors[1])

    ax.set_xlabel(xlabel)
    ax.grid()
    plt.title(title)
    plt.legend()
    
    if file_out is None:
        plt.show()
    else:
        plt.savefig(file_out+'.eps',format='eps',dpi=200)
        plt.close()



def plot_1ax(x,y1,y2,xlabel,ylabel,label1,label2,title,colors,file_out=None):
    """
    Plot 2 or more variables on the same axis
    To save the figure, set file_out = '/directory/for/figures/file_name'

    """
    plt.figure()
    for i in range(len(y1)):
        plt.plot(x[i], y1[i], linestyle='-', ms=4, color=colors[i],label=label2[i]+', '+label1[0])

    for i in range(len(y2)):
        plt.plot(x[i], y2[i], linestyle='-.', ms=4, color=colors[i],label=label2[i]+', '+label1[1])

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.grid()
    plt.title(title)
    plt.legend()
    plt.xlim(x[0][0],x[0][-1])
    
    if file_out is None:
        plt.show()
    else:
        plt.savefig(file_out+'.eps',format='eps',dpi=200)
        plt.close()















