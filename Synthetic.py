# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 12:43:59 2022

@author: Asus
"""

import ImplementFunc as func
import pandas as pd

# singapore synthetic rainfall data
df = pd.read_csv('SyntheticRainfall1.txt', sep = '\t', 
                           names = ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Rainfall_mm'])

# taking data in day, evenly distribute the 5-minute value into 300 seconds 
y1rainfall = df[df['Year'] == 1].loc[178:190,'Rainfall_mm']*1e-3*554*0.9 # m^3 (178:467)
inputdata = y1rainfall.loc[y1rainfall.index.repeat(300)] # 300 seconds in 5 minutes
inputdata = inputdata.map(lambda x: x/300)

# fixed demand
demand = pd.Series(0, index = range(len(inputdata))) # m^3
demand[len(inputdata)/2] = 8.36 

# system components (fixed parameters)
tank_param = {'main': {'area': 1.44, 'height': 1.5, 'initlevel': 0.0}, 
              'detention': {'area': 1.44, 'height': 2.0, 'initlevel': 0.0},
              'harvesting': {'area': 1.44, 'height': 2.0, 'initlevel': 0.0}}

orifice_param = {'mainOri': {'height': 0.0, 'amax': 0.02, 'amin': 0.0},
                 'mainharvOri': {'height': 0.5, 'amax': 0.05, 'amin': 0.0},
                 'detOri': {'height': 0.0, 'amax': 0.01, 'amin': 0.0},
                 'harvOri': {'height': 0.0, 'amax': 0.05, 'amin': 0.0}}

weir_param = {'mainweirh': {'height': 1.3, 'length': 1.2}}

system = func.rwhsystem(inputdata, demand, tank_param, orifice_param, weir_param, 0.74)