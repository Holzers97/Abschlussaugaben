# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:07:42 2020

@author: stefa
"""
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from  mpl_toolkits.basemap import Basemap


def read_data(filename):
    """
    reads the datafile from website

    Parameters
    ----------
    filename : string
        path and filename

    Returns
    -------
    data : Dataset netCDF4._netCDF4.Dataset

    """
    data=Dataset(filename, mode= 'r')
    return data
Months=[]
def months_sp(datas):
    """
    Transforms given data into a list of seasional mean percipitation

    Parameters
    ----------
    datas : Dataset
        data returned from method read_data(filename)

    Returns
    -------
    seasons : list
        A list of mean temperature with length of 4 splitted into Season (Spring,Summer,Fall,Winter)

    """
    temp = datas.variables['prate'][372:-1]#starting month is (1979-1948)*12, end is -1 is last, last is not incl.
    temp = temp*3600*24
    mon_mean=[] # Liste mit mittelwert der temp fue jed. Monat
    for i in range(12):
        mw = np.mean(temp[i::12,:,:],axis = 0)
        mon_mean.append(mw)
    seasons=[]
    for i in range(4):
        seasons.append((mon_mean[(i*3+2)%12]+mon_mean[(i*3+3)%12]+mon_mean[(i*3+4)%12])/3)
    """
        2 3 4 Maerz bis Mai; Fruehling
        5 6 7 ... ; Sommer
        8 9 10 ...; Herbst
        11 0 1 Dez,Jan,Feb; Winter
    """
    return seasons    

def plot_stuff(datas, mean_temp):
    """
    Creates 4 plots in 1 figure to show mean percipitation for each season 
    and shows it

    Parameters
    ----------
    datas : Dataset
        data returned by method read_data(filename)
    mean_temp : list 
        Mean temperatures splitted into seasons (by months_sp)

    Returns
    -------
    None.

    """
    fig, axs = plt.subplots(2,2,figsize=(24,15))
    ses = ["Spring","Summer","Fall","Winter"]
    for row in range(2):
        for cell in range(2):     
            map = Basemap(projection="cyl", resolution='l', llcrnrlat=-90, urcrnrlat=90,llcrnrlon=0, urcrnrlon=360, ax=axs[row][cell]) 
            #map = Basemap(projection="cyl", resolution='c', llcrnrlon=-180, urcrnrlon=180) 
            map.drawcoastlines(color="black")
            lons,lats = np.meshgrid(datas.variables['lon'][:], datas.variables['lat'][:]) 
            x,y = map(lons, lats)
            map.drawparallels(np.arange(-80., 81., 10.), labels=[1,0,0,0], fontsize=13)
            map.drawmeridians(np.arange(0, 360, 360/6.), labels=[0,0,0,1], fontsize=13)
            temp_plot = map.contourf(x, y, mean_temp[row*2+cell], cmap=plt.cm.viridis) 
            cb = map.colorbar(temp_plot, "right", size="5%", pad="2%", extend = 'both')
            cb.set_label(u"$mm/d$",fontsize=24)
            plt.title("Mean Percipitation "+ses[row*2+cell])
    plt.show() 
    plt.savefig("cruts_global.png")


#Example usage
if __name__ == "__main__":
    datas_t= read_data('C:/Users/stefa/Documents/Informathik/prate.sfc.mon.mean.nc')
    month_t = months_sp(datas_t)
    plot_stuff(datas_t, month_t)
    
