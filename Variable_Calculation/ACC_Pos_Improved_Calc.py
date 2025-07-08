import xarray as xr
import numpy as np
import sys
sys.path.append('/home/users/jonros74/Coding/')
from JonTools import jon_data
from JonTools import latlon
import datetime
import cftime




#Define the model in question and the relevant variable, set up the script parameters
institution_id=sys.argv[1]
source_id=sys.argv[2]
expt_id=sys.argv[3]
variant_id=sys.argv[4]
iteration_number=int(sys.argv[5])
print(institution_id,source_id,expt_id,variant_id,iteration_number)

upper_lat=-55.49347
upper_lon=-67
data_load_path="/gws/nopw/j04/orchestra_vol1/jonros74/Met_Office_Runs/"
data_save_path="/gws/nopw/j04/orchestra_vol1/jonros74/Data_Improved/"



if jon_data.mo_check(institution_id,source_id,expt_id,variant_id,"Omon","msftbarot")[1]==1:
	msft_set=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","msftbarot")
	if institution_id=="EC-Earth-Consortium" or institution_id=="IPSL":
		msft_array=-msft_set.get("msftbarot")[iteration_number*12:(iteration_number+1)*12]
	else:	
		msft_array=msft_set.get("msftbarot")[iteration_number*12:(iteration_number+1)*12]
	msft_values=msft_array.values
	longitude=jon_data.coord_get(msft_set,"longitude")
	latitude=jon_data.coord_get(msft_set,"latitude")
	upper_index=latlon.point(msft_set,upper_lat,upper_lon)
	index_ref_set=msft_set

	if "time" in msft_set.coords:
		time_coord=msft_array.coords['time'].values
	coords={'time':time_coord}


	if "time" in msft_set.dims:
		time_dim=msft_set.dims['time']
	dims={'time':time_dim}
	if type(msft_array.time.values[0])==cftime._cftime.Datetime360Day or type(msft_array.time.values[0])==cftime._cftime.DatetimeNoLeap or type(msft_array.time.values[0])==cftime._cftime.DatetimeProlepticGregorian or type(msft_array.time.values[0])==cftime._cftime.DatetimeGregorian:
		years=str(msft_array.time.values[0].year)+"-"+str(msft_array.time.values[-1].year)
	elif type(msft_array.time.values[0])==np.datetime64:
		years=np.datetime_as_string(msft_array.time.values[0])[:4]+"-"+np.datetime_as_string(msft_array.time.values[-1])[:4]
	else:
		years=str(msft_array.time.values[0])+"-"+str(msft_array.time.values[-1])
	print(years)



elif jon_data.mo_check(institution_id,source_id,expt_id,variant_id,"Omon","uo")[1]==1:
	uo_set=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","uo")
	uo_array=uo_set.get("uo")[iteration_number*12:(iteration_number+1)*12]
	uo=uo_array.values
	lev_bnds=jon_data.var_get(uo_set,"lev_bnds")
	index_ref_set=uo_set
	if np.ndim(lev_bnds)==3:
		height=lev_bnds[:,:,1]-lev_bnds[:,:,0]
		height_tile=np.tile(np.reshape(height,(np.shape(height)[0],np.shape(height)[1],1,1)),(1,1,np.shape(uo)[2],np.shape(uo)[3]))
	elif np.ndim(lev_bnds)==2:
		height=lev_bnds[:,1]-lev_bnds[:,0]
		height_tile=np.tile(np.reshape(height,(1,np.shape(height)[1],1,1)),(np.shape(uo)[0],1,np.shape(uo)[2],np.shape(uo)[3]))

	lat_bnds=jon_data.var_get(uo_set,"lat_bnds")
	if np.ndim(lat_bnds)==2:
		width=(lat_bnds[:,1]-lat_bnds[:,0])*111*10**3
		width_tile=np.tile(np.reshape(width,(1,1,np.shape(width)[0],1)),(np.shape(uo)[0],np.shape(uo)[1],1,np.shape(uo)[3]))
	elif np.ndim(lat_bnds)==3:
		width=(np.max(lat_bnds,axis=2)-np.min(lat_bnds,axis=2))*111*10**3
		width_tile=np.tile(np.reshape(width,(1,1,np.shape(width)[1],np.shape(width)[2])),(np.shape(uo)[0],np.shape(uo)[1],1,1))
	elif np.ndim(lat_bnds)==4:
		width=(np.max(lat_bnds,axis=3)-np.min(lat_bnds,axis=3))*111*10**3
		width_tile=np.tile(np.reshape(width,(np.shape(width)[0],1,np.shape(width)[1],np.shape(width)[2])),(1,np.shape(uo)[1],1,1))
	depth_summed_vol_flux=np.nansum(uo*height_tile*width_tile,axis=1)
	msft_values=np.zeroes(np.shape(depth_summed_vol_flux)[0],np.shape(depth_summed_vol_flux)[1],np.shape(depth_summed_vol_flux)[2])
	for i in range(0,np.shape(depth_summed_values)[1]):
		msft_values[:,i,:]=np.nansum(depth_summed_vol_flux[:,:i+1,:],axis=1)

	longitude=jon_data.coord_get(uo_set,"longitude")
	latitude=jon_data.coord_get(uo_set,"latitude")
	upper_index=latlon.point(uo_set,upper_lat,upper_lon)

	if "time" in uo_set.coords:
		time_coord=uo_array.coords['time'].values
	coords={'time':time_coord}


	if "time" in uo_set.dims:
		time_dim=uo_set.dims['time']
	dims={'time':time_dim}


	if type(uo_array.time.values[0])==cftime._cftime.Datetime360Day or type(uo_array.time.values[0])==cftime._cftime.DatetimeNoLeap or type(uo_array.time.values[0])==cftime._cftime.DatetimeProlepticGregorian or type(uo_array.time.values[0])==cftime._cftime.DatetimeGregorian:
		years=str(uo_array.time.values[0].year)+"-"+str(uo_array.time.values[-1].year)
	elif type(uo_array.time.values[0])==np.datetime64:
		years=np.datetime_as_string(uo_array.time.values[0])[:4]+"-"+np.datetime_as_string(uo_array.time.values[-1])[:4]
	else:
		years=str(uo_array.time.values[0])+"-"+str(uo_array.time.values[-1])
	print(years)


#Calculate ACC strength
#Difference between lat -62.658001 lon -55 to lat -55.49347 lon -67

upper_lat_acc_calc=-55.49347
upper_lon_acc_calc=-67
lower_lat_acc_calc=-62.658001
lower_lon_acc_calc=-55

upper_index_acc_calc=latlon.point(index_ref_set,upper_lat_acc_calc,upper_lon_acc_calc)
lower_index_acc_calc=latlon.point(index_ref_set,lower_lat_acc_calc,lower_lon_acc_calc)

msft=msft_values
if len(upper_index_acc_calc)==2:
	if np.isnan(msft[0,upper_index_acc_calc[0],upper_index_acc_calc[1]])==True:
		i=1

		while np.isnan(msft[0,upper_index_acc_calc[0],upper_index_acc_calc[1]])==True:
			upper_index_acc_calc[0]=upper_index_acc_calc[0]-1

	if np.isnan(msft[0,lower_index_acc_calc[0],lower_index_acc_calc[1]])==True:
		i=1

		while np.isnan(msft[0,lower_index_acc_calc[0],lower_index_acc_calc[1]])==True:
			lower_index_acc_calc[0]=lower_index_acc_calc[0]-1

elif len(upper_index_acc_calc)==3:
	if np.isnan(msft[upper_index_acc_calc[0],upper_index_acc_calc[1],upper_index_acc_calc[2]])==True:
		i=1

		while np.isnan(msft[upper_index_acc_calc[0],upper_index_acc_calc[1],upper_index_acc_calc[2]])==True:
			upper_index_acc_calc[1]=upper_index_acc_calc[1]-1

	if np.isnan(msft[lower_index_acc_calc[0],lower_index_acc_calc[1],lower_index_acc_calc[2]])==True:
		i=1

		while np.isnan(msft[lower_index_acc_calc[0],lower_index_acc_calc[1],lower_index_acc_calc[2]])==True:
			lower_index_acc_calc[1]=lower_index_acc_calc[1]-1




print(upper_index_acc_calc, lower_index_acc_calc, np.shape(longitude),np.shape(latitude))
if len(upper_index_acc_calc)==2 and np.ndim(latitude)==2:
	print(latitude[lower_index_acc_calc[0],lower_index_acc_calc[1]],longitude[lower_index_acc_calc[0],lower_index_acc_calc[1]],latitude[upper_index_acc_calc[0],upper_index_acc_calc[1]],longitude[upper_index_acc_calc[0],upper_index_acc_calc[1]])
	upper_value=msft[:,upper_index_acc_calc[0],upper_index_acc_calc[1]]
	lower_value=msft[:,lower_index_acc_calc[0],lower_index_acc_calc[1]]
elif len(upper_index_acc_calc)==2 and np.ndim(latitude)==1:
	print(latitude[lower_index_acc_calc[0]],longitude[lower_index_acc_calc[1]],latitude[upper_index_acc_calc[0]],longitude[upper_index_acc_calc[1]])
	upper_value=msft[:,upper_index_acc_calc[0],upper_index_acc_calc[1]]
	lower_value=msft[:,lower_index_acc_calc[0],lower_index_acc_calc[1]]
elif len(upper_index_acc_calc)==2 and np.ndim(latitude)==3:
	print(latitude[0,lower_index_acc_calc[0],lower_index_acc_calc[1]],longitude[0,lower_index_acc_calc[0],lower_index_acc_calc[1]],latitude[0,upper_index_acc_calc[0],upper_index_acc_calc[1]],longitude[0,upper_index_acc_calc[0],upper_index_acc_calc[1]])
	upper_value=msft[:,upper_index_acc_calc[0],upper_index_acc_calc[1]]
	lower_value=msft[:,lower_index_acc_calc[0],lower_index_acc_calc[1]]


elif len(upper_index_acc_calc)==3:
	print(latitude[lower_index_acc_calc[0],lower_index_acc_calc[1],lower_index_acc_calc[2]],longitude[lower_index_acc_calc[0],lower_index_acc_calc[1],lower_index_acc_calc[2]],latitude[upper_index_acc_calc[0],upper_index_acc_calc[1],upper_index_acc_calc[2]],longitude[upper_index_acc_calc[0],upper_index_acc_calc[1],upper_index_acc_calc[2]])

	upper_value=msft[:,upper_index_acc_calc[1],upper_index_acc_calc[2]]
	lower_value=msft[:,lower_index_acc_calc[1],lower_index_acc_calc[2]]



ACC=(lower_value-upper_value)/10**9

acc_array=xr.DataArray(ACC,dims=('time'),coords={'time':msft_array.coords['time']})









southern_value=np.nanmin(np.nanmax(msft_values,axis=1),axis=(1))
northern_value=np.nanmin(msft_values[:,:upper_index[0],upper_index[1]],axis=1)
mid_value=np.nanmean((southern_value,northern_value),axis=0)

southern_latitude=np.zeros(np.shape(msft_values)[2])
southern_mean_latitude=np.zeros(np.shape(msft_values)[0])

northern_latitude=np.zeros(np.shape(msft_values)[2])
northern_mean_latitude=np.zeros(np.shape(msft_values)[0])

mid_latitude=np.zeros(np.shape(msft_values)[2])
mid_mean_latitude=np.zeros(np.shape(msft_values)[0])


for i in range(0,np.shape(msft_values)[0]):
	southern_diff=abs(msft_values[i,:,:]-southern_value[i])
	northern_diff=abs(msft_values[i,:,:]-northern_value[i])
	mid_diff=abs(msft_values[i,:,:]-mid_value[i])
	for j in range(0,np.shape(msft_values)[2]):
		southern_pos=np.where(np.nanmin(southern_diff[:,j])==southern_diff[:,j])[0][0]
		southern_latitude[j]=latitude[southern_pos,j]
		try:
			northern_pos=np.nanmin(np.where(msft_values[i,:,j]<northern_value[i]))
			#northern_pos=np.where(np.nanmin(northern_diff[:,j])==northern_diff[:,j])[0][0]
			northern_latitude[j]=latitude[northern_pos,j]
		except:
			northern_latitude[j]=np.nan
		mid_pos=np.where(np.nanmin(mid_diff[:,j])==mid_diff[:,j])[0][0]
		mid_latitude[j]=latitude[mid_pos,j]
		print(northern_latitude[j])
	southern_mean_latitude[i]=np.nanmean(southern_latitude)
	northern_mean_latitude[i]=np.nanmean(northern_latitude)
	mid_mean_latitude[i]=np.nanmean(mid_latitude)


southern_array=xr.DataArray(southern_mean_latitude,dims=dims,coords=coords,name="saccpos")
south_description="Mean latitude of the most southerly circumpolar streamfunction contour"
jon_data.save(data_array=southern_array,data_path=data_save_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="saccpos",var_long_name="Southern ACC Position",var_description=south_description,units="degrees",freq="mon",spatial="sin",years=years)



northern_array=xr.DataArray(northern_mean_latitude,dims=dims,coords=coords,name="naccpos")
north_description="Mean latitude of the most northerly circumpolar streamfunction contour"
jon_data.save(data_array=northern_array,data_path=data_save_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="naccpos",var_long_name="Northern ACC Position",var_description=north_description,units="degrees",freq="mon",spatial="sin",years=years)




mid_array=xr.DataArray(mid_mean_latitude,dims=dims,coords=coords,name="maccpos")
mid_description="Mean latitude of the central circumpolar streamfunction contour"
jon_data.save(data_array=mid_array,data_path=data_save_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="maccpos",var_long_name="Central ACC Position",var_description=mid_description,units="degrees",freq="mon",spatial="sin",years=years)


acc_description="This is the ACC strength in Sverdrups. It is derived by taking the difference of two points on either side of Drake Passage."
jon_data.save(data_array=acc_array,data_path=data_save_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="acc",var_long_name="ACC Strength",var_description=acc_description,units="Sv",freq="mon",spatial="sin",years=years)
















