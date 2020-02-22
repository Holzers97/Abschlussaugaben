# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:28:45 2020

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
    
def mean_temp(datas):
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
    temp_19=datas.variables['air'][841:-1]
    temp_19 -= 273
    #takes mean for each time with fix lat and lon.
    temp_19_m = np.mean(temp_19[:,:,:],axis = 0)
    return temp_19_m
    
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
    plt.figure(figsize=(18,16))
    map = Basemap(projection="cyl", resolution='l', llcrnrlat=46, urcrnrlat=49,llcrnrlon=9, urcrnrlon=17) 
    #map = Basemap(projection="cyl", resolution='c', llcrnrlon=-180, urcrnrlon=180) 
    map.drawcountries()
    map.drawcoastlines(color="black")
    lons,lats = np.meshgrid(datas.variables['lon'][:], datas.variables['lat'][:]) 
    x,y = map(lons, lats)
    map.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=13)
    map.drawmeridians(np.arange(0, 360, 360/6.), labels=[0,0,0,1], fontsize=13)
    
    
    temp_plot = map.contourf(x, y, mean_temp, cmap=plt.cm.viridis) 
    cb = map.colorbar(temp_plot, "right", size="5%", pad="2%", extend = 'both')
    cb.set_label(u"Temperature \u2103",fontsize=24)
    plt.title("Mean Temperature (1979-2019)",fontdict={'fontsize':24})
    #plt.annotate('Data - CRU TS v4.02',(-178,-88), fontsize=12)
    plt.show() 
    plt.savefig("cruts_global.png")
    
    
if __name__=="__main__":
    daten = read_data('C:/Users/stefa/Documents/Informathik/air.2m.mon.mean-1.nc')
    avg_temp = mean_temp(daten)
    plot_stuff(daten,avg_temp)

