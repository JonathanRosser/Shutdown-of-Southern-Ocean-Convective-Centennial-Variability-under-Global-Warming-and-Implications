import xarray as xr
import numpy as np
import sys
sys.path.append('/home/users/jonros74/Coding/')
from JonTools import jon_data
from JonTools import latlon
import gsw
import cftime

#Define the model in question and the relevant variable, set up the script parameters
institution_id=sys.argv[1]
source_id=sys.argv[2]
expt_id=sys.argv[3]
variant_id=sys.argv[4]
iteration_number=int(sys.argv[5])
print(institution_id,source_id,expt_id,variant_id,iteration_number)


data_load_path="/gws/nopw/j04/orchestra_vol1/jonros74/Met_Office_Runs/"
data_save_path="/gws/nopw/j04/orchestra_vol1/jonros74/Data_Improved/"



if jon_data.mo_check(institution_id,source_id,expt_id,variant_id,"Omon","tauuo")[1]==1:  

	print("Using tauuo")
	wind_dataset=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","tauuo")
	wind_array=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","tauuo").tauuo[iteration_number*12:(iteration_number+1)*12]
	if type(wind_array.time.values[0])==cftime._cftime.Datetime360Day or type(wind_array.time.values[0])==cftime._cftime.DatetimeNoLeap or type(wind_array.time.values[0])==cftime._cftime.DatetimeProlepticGregorian or type(wind_array.time.values[0])==cftime._cftime.DatetimeGregorian:
		years=str(wind_array.time.values[0].year)+"-"+str(wind_array.time.values[-1].year)
	elif type(wind_array.time.values[0])==np.datetime64:
		years=np.datetime_as_string(wind_array.time.values[0])[:4]+"-"+np.datetime_as_string(wind_array.time.values[-1])[:4]
	else:
		years=str(wind_array.time.values[0])+"-"+str(wind_array.time.values[-1])
	print(years)


	tauuo=wind_array.values
	latitude=jon_data.coord_get(wind_dataset,"latitude")
	if latitude.ndim==2:
		mean_latitude=np.nanmean(latitude,axis=-1)
	elif latitude.ndim==1:
		mean_latitude=latitude
	elif latitude.ndim==3:
		mean_latitude=np.nanmean(latitude,axis=(0,2))

	mask=latlon.area(wind_dataset,maxlat=0)

	masked_wind=np.multiply(tauuo,mask)
	emask=latlon.area(wind_dataset,maxlat=-50)
	emasked_wind=np.multiply(tauuo,emask)
	zonal_average=np.nanmean(masked_wind,axis=2)
	ezonal_average=np.nanmean(emasked_wind,axis=2)
	max_wind=np.nanmax(zonal_average,axis=1)
	min_wind=np.nanmin(ezonal_average,axis=1)
	max_wind_position=np.zeros(np.shape(max_wind))
	min_wind_position=np.zeros(np.shape(max_wind))
	for i in range(0,np.shape(max_wind)[0]):
	    max_wind_position[i]=mean_latitude[np.where(zonal_average[i,:]==max_wind[i])[0][0]]
	    min_wind_position[i]=mean_latitude[np.where(zonal_average[i,:]==min_wind[i])[0][0]]




	if "time" in wind_dataset.coords:
		time_coord=wind_dataset.coords['time'][iteration_number*12:(iteration_number+1)*12].values


	coords={'time':time_coord}


	if "time" in wind_dataset.dims:
		time_dim=wind_dataset.dims['time']

	dims={'time':time_dim}

	wwmax_array=xr.DataArray(max_wind,dims=dims,coords=coords,name='wwmax')
	wwpos_array=xr.DataArray(max_wind_position,dims=dims,coords=coords,name='wwpos')

	ewmax_array=xr.DataArray(min_wind,dims=dims,coords=coords,name='ewmax')
	ewpos_array=xr.DataArray(min_wind_position,dims=dims,coords=coords,name='ewpos')

	wwmax_description="Magnitude of the maximum zonally averaged westerly wind stress in the Southern Hemisphere."
	ewmax_description="Magnitude of the maximum zonally averaged Easterly wind stress in the Southern Hemisphere."

	wwpos_description="Latitude of the maximum zonally averaged westerly wind stress in the Southern Hemisphere."
	ewpos_description="Latitude of the maximum zonally averaged Easterly wind stress in the Southern Hemisphere."


	jon_data.save(data_array=wwmax_array,data_path=data_save_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="wwmax", var_long_name="Westerly Wind Maximum Magnitude",var_description=wwmax_description,units="Nm^(-2)",freq="mon",spatial="sin",years=years)

	jon_data.save(data_array=ewmax_array,data_path=data_save_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="ewmax", var_long_name="Easterly Wind Maximum Magnitude",var_description=ewmax_description,units="Nm^(-2)",freq="mon",spatial="sin",years=years)

	jon_data.save(data_array=wwpos_array,data_path=data_save_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="wwpos", var_long_name="Westerly Wind Maximum Position",var_description=wwpos_description,units="degrees_north",freq="mon",spatial="sin",years=years)

	jon_data.save(data_array=ewpos_array,data_path=data_save_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="ewpos", var_long_name="Easterly Wind Maximum Position",var_description=ewpos_description,units="degrees_north",freq="mon",spatial="sin",years=years)


elif jon_data.mo_check(institution_id,source_id,expt_id,variant_id,"Amon","tauu")[1]==1:

        print("Using tauu")
        wind_array=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Amon","tauu")[iteration_number*12:(iteration_number+1)*12]

        if type(wind_array.time.values[0])==cftime._cftime.Datetime360Day or type(wind_array.time.values[0])==cftime._cftime.DatetimeNoLeap or type(wind_array.time.values[0])==cftime._cftime.DatetimeProlepticGregorian or type(wind_array.time.values[0])==cftime._cftime.DatetimeGregorian:
                years=str(wind_array.time.values[0].year)+"-"+str(wind_array.time.values[-1].year)
        elif type(wind_array.time.values[0])==np.datetime64:
                years=np.datetime_as_string(wind_array.time.values[0])[:4]+"-"+np.datetime_as_string(wind_array.time.values[-1])[:4]
        else:
                years=str(wind_array.time.values[0])+"-"+str(wind_array.time.values[-1])
        print(years)



        tauuo=wind_array.get("tauu").values

        if "lat" in wind_array.coords:
                latitude=wind_array.get('lat').values
        elif "latitude" in wind_array.coords:
                latitude=wind_array.get('latitude').values
        elif "j" in wind_array.coords:
                latitude=wind_array.get('j').values
        if latitude.ndim==2:
                mean_latitude=np.nanmean(latitude,axis=-1)
        elif latitude.ndim==1:
                mean_latitude=latitude


        mask=latlon.area(wind_array,maxlat=0)

        masked_wind=np.multiply(tauuo,mask)
        zonal_average=np.nanmean(masked_wind,axis=2)
        max_wind=np.nanmax(zonal_average,axis=1)
        min_wind=np.nanmin(zonal_average,axis=1)
        max_wind_position=np.zeros(np.shape(max_wind))
        min_wind_position=np.zeros(np.shape(max_wind))
        for i in range(0,np.shape(max_wind)[0]):
            max_wind_position[i]=mean_latitude[np.where(zonal_average[i,:]==max_wind[i])[0][0]]
            min_wind_position[i]=mean_latitude[np.where(zonal_average[i,:]==min_wind[i])[0][0]]




        if "time" in wind_array.coords:
                time_coord=wind_array.coords['time'].values


        coords={'time':time_coord}


        if "time" in wind_array.dims:
                time_dim=wind_array.dims['time']

        dims={'time':time_dim}

        wwmax_array=xr.DataArray(max_wind,dims=dims,coords=coords,name='wwmax')
        wwpos_array=xr.DataArray(max_wind_position,dims=dims,coords=coords,name='wwpos')

        ewmax_array=xr.DataArray(min_wind,dims=dims,coords=coords,name='ewmax')
        ewpos_array=xr.DataArray(min_wind_position,dims=dims,coords=coords,name='ewpos')

        wwmax_description="Magnitude of the maximum zonally averaged westerly wind stress in the Southern Hemisphere. Using tauu."
        ewmax_description="Magnitude of the maximum zonally averaged Easterly wind stress in the Southern Hemisphere. Using tauu."

        wwpos_description="Latitude of the maximum zonally averaged westerly wind stress in the Southern Hemisphere. Using tauu."
        ewpos_description="Latitude of the maximum zonally averaged Easterly wind stress in the Southern Hemisphere. Using tauu."


        jon_data.save(data_array=wwmax_array,data_path=data_save_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="wwmax", var_long_name="Westerly Wind Maximum Magnitude",var_description=wwmax_description,units="Nm^(-2)",freq="mon",spatial="sin",years=years)

        jon_data.save(data_array=ewmax_array,data_path=data_save_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="ewmax", var_long_name="Easterly Wind Maximum Magnitude",var_description=ewmax_description,units="Nm^(-2)",freq="mon",spatial="sin",years=years)

        jon_data.save(data_array=wwpos_array,data_path=data_save_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="wwpos", var_long_name="Westerly Wind Maximum Position",var_description=wwpos_description,units="degrees_north",freq="mon",spatial="sin",years=years)

        jon_data.save(data_array=ewpos_array,data_path=data_save_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="ewpos", var_long_name="Easterly Wind Maximum Position",var_description=ewpos_description,units="degrees_north",freq="mon",spatial="sin",years=years)


else:
	print("Neither tauuo or tauu found")

