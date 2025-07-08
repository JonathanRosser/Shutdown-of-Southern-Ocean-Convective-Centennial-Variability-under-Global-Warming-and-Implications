import xarray as xr 
import numpy as np 
import sys
sys.path.append('/home/users/jonros74/Coding/')
from JonTools import jon_data


def area(data,minlat=None,maxlat=None,minlon=None,maxlon=None):
    #This function takes an xarray dataframe and will create a mask which can be passed over a dataset to select the specific range of latitudes and longitudes
    longitude=jon_data.coord_get(data,"longitude")


    if np.max(longitude)>180:
       longitude=np.mod(longitude+180,360)-180
    
    latitude=jon_data.coord_get(data,"latitude")

    if np.ndim(longitude)==1 and np.ndim(latitude)==1:
        lat_len=len(latitude)
        lon_len=len(longitude)
        if minlat!=None and maxlat!=None:
            latitude_mask=np.tile(np.reshape(((latitude>=minlat)&(latitude<=maxlat)),(lat_len,1)),(1,lon_len))
        elif minlat!=None and maxlat==None:
            latitude_mask=np.tile(np.reshape((latitude>=minlat),(lat_len,1)),(1,lon_len))
        elif minlat==None and maxlat!=None:
            latitude_mask=np.tile(np.reshape((latitude<=maxlat),(lat_len,1)),(1,lon_len))
        elif minlat==None and maxlat==None:
            latitude_mask=np.ones((lat_len,lon_len))
        if minlon!=None and maxlon!=None:
            longitude_mask=np.tile(np.reshape(((longitude>=minlon)&(longitude<=maxlon)),(1,lon_len)),(lat_len,1))
        elif minlon!=None and maxlon==None:
            longitude_mask=np.tile(np.reshape((longitude>=minlon),(1,lon_len)),(lat_len,1))
        elif minlon==None and maxlon!=None:
            longitude_mask=np.tile(np.reshape((longitude<=maxlon),(1,lon_len)),(lat_len,1))
        elif minlon==None and maxlon==None:
            longitude_mask=np.ones((lat_len,lon_len))

    else:
        if minlat!=None and maxlat!=None:
             latitude_mask=(latitude>=minlat)&(latitude<=maxlat)
        elif minlat!=None and maxlat==None:
             latitude_mask=latitude>=minlat
        elif minlat==None and maxlat!=None:
             latitude_mask=latitude<=maxlat
        elif minlat==None and maxlat==None:
             latitude_mask=np.ones(np.shape(latitude))
        if minlon!=None and maxlon!=None:
             longitude_mask=(longitude>=minlon)&(longitude<=maxlon)
        elif minlon!=None and maxlon==None:
             longitude_mask=longitude>=minlon
        elif minlon==None and maxlon!=None:
             longitude_mask=longitude<=maxlon
        elif minlon==None and maxlon==None:
             longitude_mask=np.ones(np.shape(longitude))
    final_mask=np.multiply(latitude_mask,longitude_mask)
    return final_mask

def findnearest(array,number,axis=None ):
    #This function will find the index of the number closest to the desired number in an array
    diff=np.abs(array-number)
    if axis==None:
        index=np.unravel_index(np.argmin(diff,axis=axis),diff.shape)
    else:
        index=np.argmin(diff,axis=axis)
    return index

def point(data,lat,lon):
    #This function will retrieve the point closest to the given latitude and longitude
    longitude=jon_data.coord_get(data,"longitude")

    if np.max(longitude)>180:
       longitude=np.mod(longitude+180,360)-180
    latitude=jon_data.coord_get(data,"latitude")
    lon_diff=np.abs(longitude-lon)
    lat_diff=np.abs(latitude-lat)
    if np.ndim(lon_diff)==2 and np.ndim(lat_diff)==2:
        total_diff=np.sqrt(lon_diff**2+lat_diff**2)
    elif np.ndim(lon_diff)==3 and np.ndim(lat_diff)==3:
        total_diff=np.sqrt(np.nanmean(lon_diff,axis=0)**2+np.nanmean(lat_diff,axis=0)**2)
    elif np.ndim(lon_diff)==1 and np.ndim(lat_diff)==1:
        lon_diff_tile=np.tile(np.reshape(lon_diff,(1,len(lon_diff))),(len(lat_diff),1))
        lat_diff_tile=np.tile(np.reshape(lat_diff,(len(lat_diff),1)),(1,len(lon_diff)))
        total_diff=np.sqrt(lon_diff_tile**2+lat_diff_tile**2)
    index=np.unravel_index(np.argmin(total_diff),total_diff.shape)
    result=np.array(index)
    #final_mask=np.zeros(np.shape(longitude))
    #final_mask[index]=1
    return result


def latline(data,lat,minlon=-180,maxlon=180,tolerance=5):
    #This function will retrieve a line of constant latitude within a range of longitude values
    longitude=jon_data.coord_get(data,"longitude")
    latitude=jon_data.coord_get(data,"latitude")
    longitude_mask=(longitude>=minlon)&(longitude<=maxlon)
    latitude_mask=(latitude>=lat-tolerance)&(latitude<=latitude+tolerance)
    initial_mask=np.multiply(longitude_mask,latitude_mask)
    lon_mask=np.multiply(latitude,initial_mask)
    indices=findnearest(lon_mask,lat,axis=0)
    other_indices=np.arange(len(indices))
    latitude_mask_second=np.zeros(np.shape(longitude))
    latitude_mask_second[indices,other_indices]=1
    final_mask=np.multiply(latitude_mask_second,initial_mask)
    return final_mask

def lonline(data,lon,minlat=-90,maxlat=90,tolerance=5):
    #This function will retrieve a line of constant longitude within a range of latitude values
    longitude=jon_data.coord_get(data,"longitude")
    latitude=jon_data.coord_get(data,"latitude")

    longitude_mask=(longitude>=lon-tolerance)&(longitude<=lon+tolerance)
    latitude_mask=(latitude>=minlat)&(latitude<=maxlat)
    initial_mask=np.multiply(longitude_mask,latitude_mask)
    lon_mask=np.multiply(longitude,initial_mask)
    indices=findnearest(lon_mask,lon,axis=1)
    other_indices=np.arange(len(indices))
    longitude_mask_second=np.zeros(np.shape(longitude))
    longitude_mask_second[other_indices,indices]=1
    final_mask=np.multiply(longitude_mask_second,initial_mask)
    return final_mask



