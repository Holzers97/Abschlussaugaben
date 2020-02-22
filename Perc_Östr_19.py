# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:57:58 2020

@author: stefa
"""
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from  mpl_toolkits.basemap import Basemap


def read_data(filename):
    '''
    reads the data from website

Parameters
    ----------
    filename : strg
        path and filename

Returns
    -------
    data : Dataset netCDF4._netCDF4.Dataset
            

'''
    data=Dataset(filename, mode= 'r')
    return data
    
def mean_per(datas):
    """
    returns mean temperature of the data from 1979 - 2019


Parameters
    ----------
    datas : Dataset netCDF4._netCDF4.Dataset
        raw data from read_data(filename) method

Returns
    -------
    temp_av_1979_2019 : MaskedArray
        mean value for given data

"""
    runof = datas.variables['prate'][841:-1]
    runof= runof*3600*24#umrechnung mm pro tag
    #takes mean for each time with fix lat and lon.
    runof_1979_2019= np.mean(runof[:,:,:],axis = 0)
    return runof_1979_2019
    
def plot_stuff(datas, mean_temp):
    """
        

Parameters
    ----------
    datas : netCDF4._netCDF4.Dataset
        raw data from input file returned by read_data(filename)
    mean_temp : MaskedArray
    DESCRIPTION.

Returns
    -------
    None.

"""
    plt.figure(figsize=(24,16))
    map = Basemap(projection="cyl", resolution='l', llcrnrlat=46, urcrnrlat=49,llcrnrlon=9, urcrnrlon=17, ) 
    #map = Basemap(projection="cyl", resolution='c', llcrnrlon=-180, urcrnrlon=180) 
    map.drawcoastlines(color="black") 
    map.drawcountries()
    lons,lats = np.meshgrid(datas.variables['lon'][:], datas.variables['lat'][:]) 
    x,y = map(lons, lats)
    map.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=12)
    map.drawmeridians(np.arange(0, 360, 360/6.), labels=[0,0,0,1], fontsize=12)
    
    temp_plot = map.contourf(x, y, mean_temp, cmap=plt.cm.viridis) 
    cb = map.colorbar(temp_plot, "right", size="5%", pad="2%", extend = 'both')
    cb.set_label(u"$mm/d$",fontsize=24)
    plt.title("Niederschlag 2019 Österreich",fontsize=24)
    #plt.annotate('Data - CRU TS v4.02',(-178,-88), fontsize=6)
    plt.show() 
    #plt.savefig("cruts_global.png")
    
    
if __name__=="__main__":
    daten = read_data('C:/Users/stefa/Documents/Informathik/prate.sfc.mon.mean.nc')
    avg_temp = mean_per(daten)
    plot_stuff(daten,avg_temp)
    daten.close()

