# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 20:49:11 2022

@author: yienpuah
"""

import watertankoop as wt
import matplotlib.pyplot as plt
import numpy as np
    
# --- Function to build the system configuration, plots with performance indicators
def rwhsystem (inputdata, demand, tankparams, orifice_param, weir_param, waterprice):
    
    # declare system components (tank sizes are fixed in this case)
    
    # tank
    maintank = wt.watertank('main', **tankparams['main'])
    dettank = wt.watertank('detention', **tankparams['detention'])
    harvtank = wt.watertank('harvesting', **tankparams['harvesting'])    
    
    # orifice
    mainorifice = wt.controlled('mainOri', sourcetank = maintank, destank = dettank, **orifice_param['mainOri'])
    mhorifice = wt.controlled('mainharvOri', sourcetank = maintank, destank = harvtank, **orifice_param['mainharvOri'])
    detorifice = wt.controlled('detOri', sourcetank = dettank, destank = 'public', **orifice_param['detOri'])
    # harvpump = wt.pump('harvPump', sourcetank = harvtank, destank = 'demand', **orifice_param['harvestPump'])
    harvori = wt.controlled('harvOri', sourcetank = harvtank, destank = 'demand', **orifice_param['harvOri'])
    
    # weir
    mainh_weir = wt.weir('mainweirh', **weir_param['mainweirh'], sourcetank = maintank, destank = harvtank)
    #harvweir = wt.weir('harvestweir', **weir_param['harvestweir'], sourcetank = harvtank, destank = dettank)
    
    Qsupply = [0]
    
    # of = outflow
    for i in inputdata:
        maininflow = np.array([i])
        
        # main to detention through orifice
        md_oriof = [mainorifice.computeflow(mainorifice.relay(0.8*maintank.tkhght, 0.2*maintank.tkhght))] # m^3/s convert to m^3/day 
        mh_oriof = [mhorifice.computeflow(mhorifice.passive())] # relay(0.6*maintank.tkhght, 0.2*maintank.tkhght))]
        mainh_weirof = [mainh_weir.computeflow(maintank)] # main to harvesting tank
        main_totalof = [x + y + z for x, y, z in zip(md_oriof, mh_oriof, mainh_weirof)] # main tank total outflow
        
        
        # harvesting tank
        harvinflow = [x + y for x, y in zip(mainh_weirof, mh_oriof)]
        harv_oriof = [harvori.computeflow(harvori.passive())]
        # harv_oriof = [harvpump.relay(1.7/2.46*harvtank.tkhght, 0.5/2.46*harvtank.tkhght)] # to demand
        Qsupply += harv_oriof
        
        # detention tank
        detinflow = md_oriof
        detof = [detorifice.computeflow(detorifice.passive())] # to public drainage
        

        # calculate new waterlevel in each tank (append to waterlevel array)
        maintank.massbalance(maininflow, main_totalof) 
        dettank.massbalance(detinflow, detof)
        harvtank.massbalance(harvinflow, harv_oriof)
    
    # --- Plots
    plt.figure()
    wt.plothv([maintank, dettank, harvtank])
   
    plt.figure()
    wt.plotq([mainorifice, mhorifice, detorifice, harvori, mainh_weir])
        
    print('Total water demand:', sum(demand), 'm^3')
    print('Total water supply:', sum(Qsupply), 'm^3')
    
    # --- Performance Evaluation
    wse = sum(Qsupply)/(sum(demand)*0.75)
    print('Water Saving Efficiency (WSE): ', round(wse, 6))
    
    rue = sum(Qsupply)/sum(inputdata)
    print('Rainwater Use Efficiency (RUE): ', round(rue, 6))
    
    cost_saved = sum(Qsupply)*waterprice
    print('Total cost saved: £', round(cost_saved, 6))
    
    # --- Visualise the system
    #wt.GenerateConfigurationFigure([maintank, dettank, harvtank], [mainorifice, mhorifice, detorifice, harvorifice, mainh_weir])
    