# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 17:31:49 2020

@author: stefa
"""
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap 


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
    temp = datas.variables['air'][372:-1]#starting month is (1979-1948)*12, end is -1 is last, last is not incl.
    temp -= 273
    #takes mean for each time with fix lat and lon.
    temp_av_1979_2019= np.mean(temp[:,:,:],axis = 0)
    temp_19=datas.variables['air'][841:-1]
    temp_19 -= 273
    temp_19_m = np.mean(temp_19[:,:,:],axis = 0)
    temp_diff = temp_19_m - temp_av_1979_2019
    return temp_diff
    
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
    plt.figure(figsize=(20,12))
    map = Basemap(projection="cyl", resolution='i', llcrnrlat=-90, urcrnrlat=90,llcrnrlon=0, urcrnrlon=359, ) 
    #map = Basemap(projection="cyl", resolution='c', llcrnrlon=-180, urcrnrlon=180) 
    map.drawcoastlines(color="black") 
    lons,lats = np.meshgrid(datas.variables['lon'][:], datas.variables['lat'][:]) 
    x,y = map(lons, lats)
    map.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=12)
    map.drawmeridians(np.arange(0, 360, 360/6.), labels=[0,0,0,1], fontsize=12)
    
    temp_plot = map.contourf(x, y, mean_temp, cmap=plt.cm.viridis) 
    cb = map.colorbar(temp_plot, "right", size="10%", pad="2%", extend = 'both')
    cb.set_label(u"Temperature \u2103",fontsize=24)
    plt.title("Mean Temperature (1979-2019) compared with 2019s Temperature",fontdict={'fontsize':24})
    plt.annotate('Data - CRU TS v4.02',(-178,-88), fontsize=6)
    plt.show() 
    plt.savefig("cruts_global.png")
    
if __name__=="__main__":
    daten = read_data('C:/Users/stefa/Documents/Informathik/air.2m.mon.mean-1.nc')
    avg_temp = mean_temp(daten)
    plot_stuff(daten,avg_temp)

