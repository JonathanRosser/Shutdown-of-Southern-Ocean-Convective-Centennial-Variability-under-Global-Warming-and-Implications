#Import Relevant packages

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
print(institution_id,source_id,expt_id,variant_id)

if jon_data.jasmin_check(institution_id,source_id,expt_id,variant_id,"SImon","siconc")[1]==1:	
	print("Calculate Siconc")


	siconc_array=jon_data.cmip6_load(institution_id,source_id,expt_id,variant_id,"SImon","siconc")


	siconc=siconc_array.get("siconc")[:,:,:].values

	if source_id=="CNRM-CM6-1" or source_id=="CNRM-ESM2-1":
		areacello=jon_data.cmip6_load(institution_id,source_id,"piControl","r1i1p1f2","Ofx","areacello").areacello.values
	elif source_id=="CanESM5":
		areacello=jon_data.cmip6_load(institution_id,source_id,"esm-piControl","r1i1p1f1","Ofx","areacello").areacello.values
	elif source_id=="BCC-ESM1":
		areacello=xr.open_dataset("/badc/cmip6/data/CMIP6/CMIP/BCC/BCC-ESM1/1pctCO2/r1i1p1f1/Ofx/areacello/gn/latest/areacello_Ofx_BCC-ESM1_1pctCO2_r1i1p1f1_gn.nc").areacello.values
	elif source_id=="UKESM1-0-LL":
		areacello=jon_data.cmip6_load(institution_id,source_id,"piControl","r1i1p1f2","Ofx","areacello").areacello.values
	else:
		areacello=jon_data.cmip6_load(institution_id,source_id,"piControl","r1i1p1f1","Ofx","areacello").areacello.values



	long_area=np.tile(areacello,(np.shape(siconc)[0],1,1))

	siconc_weight=siconc*long_area

	#Define a mask south of 50S
	area_mask=latlon.area(siconc_array,maxlat=-50)

	siconc50=siconc_weight*area_mask

	SI=np.nansum(siconc50,axis=(1,2))

	SI_array=xr.DataArray(SI,dims=('time'),coords={'time':siconc_array.coords['time'].astype(datetime.datetime)},name='siarea')

	var_description="This is the sea ice area below 50S."

	data_path="/gws/nopw/j04/orchestra_vol2/jonros74/Data_Improved/"
	thetao_array=jon_data.cmip6_load(institution_id,source_id,expt_id,variant_id,"Omon","thetao")

	if type(thetao_array.time.values[0])==cftime._cftime.Datetime360Day or type(thetao_array.time.values[0])==cftime._cftime.DatetimeNoLeap or type(thetao_array.time.values[0])==cftime._cftime.DatetimeProlepticGregorian or type(thetao_array.time.values[0])==cftime._cftime.DatetimeGregorian:
		years=str(thetao_array.time.values[0].year)+"-"+str(thetao_array.time.values[-1].year)
	elif type(thetao_array.time.values[0])==np.datetime64:
		years=np.datetime_as_string(thetao_array.time.values[0])[:4]+"-"+np.datetime_as_string(thetao_array.time.values[-1])[:4]
	else:
		years=str(thetao_array.time.values[0])+"-"+str(thetao_array.time.values[-1])
	print(years)


	jon_data.save(data_array=SI_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="siarea",var_long_name="Sea Ice Area below 50S", var_description=var_description,units="K",freq="mon",spatial="sin",years=years)

elif jon_data.jasmin_check(institution_id,source_id,expt_id,variant_id,"SImon","sivol")[1]==1:


	sivol_array=jon_data.cmip6_load(institution_id,source_id,expt_id,variant_id,"SImon","sivol")


	sivol=sivol_array.get("sivol")[:,:,:].values
	if source_id=="CNRM-CM6-1" or source_id=="CNRM-ESM2-1":
		areacello=jon_data.cmip6_load(institution_id,source_id,"piControl","r1i1p1f2","Ofx","areacello").areacello.values
	elif source_id=="CanESM5":
		areacello=jon_data.cmip6_load(institution_id,source_id,"esm-piControl","r1i1p1f1","Ofx","areacello").areacello.values
	elif source_id=="BCC-ESM1":
		areacello=xr.open_dataset("/badc/cmip6/data/CMIP6/CMIP/BCC/BCC-ESM1/1pctCO2/r1i1p1f1/Ofx/areacello/gn/latest/areacello_Ofx_BCC-ESM1_1pctCO2_r1i1p1f1_gn.nc").areacello.values
	elif source_id=="UKESM1-0-LL":
		areacello=jon_data.cmip6_load(institution_id,source_id,"piControl","r1i1p1f2","Ofx","areacello").areacello.values
	else:
		areacello=jon_data.cmip6_load(institution_id,source_id,"piControl","r1i1p1f1","Ofx","areacello").areacello.values


	long_area=np.tile(areacello,(np.shape(sivol)[0],1,1))

	sivol_weight=sivol*long_area

	#Define a mask south of 50S
	area_mask=latlon.area(sivol_array,maxlat=-50)

	sivol50=sivol_weight*area_mask

	SI=np.nansum(sivol50,axis=(1,2))

	SI_array=xr.DataArray(SI,dims=('time'),coords={'time':sivol_array.coords['time'].astype(datetime.datetime)},name='sivolume')

	var_description="This is the sea ice volume below 50S."

	data_path="/gws/nopw/j04/orchestra_vol2/jonros74/Data_Improved/"


	thetao_array=jon_data.cmip6_load(institution_id,source_id,expt_id,variant_id,"Omon","thetao")

	if type(thetao_array.time.values[0])==cftime._cftime.Datetime360Day or type(thetao_array.time.values[0])==cftime._cftime.DatetimeNoLeap or type(thetao_array.time.values[0])==cftime._cftime.DatetimeProlepticGregorian or type(thetao_array.time.values[0])==cftime._cftime.DatetimeGregorian:
		years=str(thetao_array.time.values[0].year)+"-"+str(thetao_array.time.values[-1].year)
	elif type(thetao_array.time.values[0])==np.datetime64:
		years=np.datetime_as_string(thetao_array.time.values[0])[:4]+"-"+np.datetime_as_string(thetao_array.time.values[-1])[:4]
	else:
		years=str(thetao_array.time.values[0])+"-"+str(thetao_array.time.values[-1])
	print(years)


	jon_data.save(data_array=SI_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="sivolume",var_long_name="Sea Ice Volume below 50S", var_description=var_description,units="K",freq="mon",spatial="sin",years=years)


else:
	print("This dataset does not have siconc or sivol")
