# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 15:33:08 2022

@author: Asus
"""

# --- Prestwick case study

import ImplementFunc as func
import pandas as pd

# read rainfall data
dataset = pd.read_excel('Prestwick_rainfall_2019.xlsx') # daily rainfall (m)

# catchment area = 606m^2
# 0.9 catchment efficiency
rainfall = dataset.loc[:, 'rainfall_m']*606*0.9 # m^3

demand_data = pd.read_excel('Prestwick_demand_2019.xlsx') # water demand (m^3)
demand = demand_data.loc[:,'demand_m3']

# system components (fixed parameters)
tank_param = {'main': {'area': 4.75, 'height': 4.0, 'initlevel': 0.0}, 
              'detention': {'area': 4.75, 'height': 4.0, 'initlevel': 0.0},
              'harvesting': {'area': 4.75, 'height': 4.0, 'initlevel': 0.0}}

orifice_param = {'mainOri': {'height': 0.0, 'amax': 0.1, 'amin': 0.0},
                 'mainharvOri': {'height': 0.8, 'amax': 0.9, 'amin': 0.0},
                 'detOri': {'height': 0.0, 'amax': 0.2, 'amin': 0.0},
                 'harvOri': {'height': 0.0, 'amax': 0.9, 'amin': 0.0}}

weir_param = {'mainweirh': {'height': 3.8, 'length': 20}}


# build system
system = func.rwhsystem(rainfall, demand, tank_param, orifice_param, weir_param, 1.38)
print('Number of days without rain:', (dataset['rainfall_m'] == 0).sum())