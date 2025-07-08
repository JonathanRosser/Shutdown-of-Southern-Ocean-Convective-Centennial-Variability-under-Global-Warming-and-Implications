import xarray as xr
import numpy as np
import sys
sys.path.append('/home/users/jonros74/Coding/')
from JonTools import jon_data
from JonTools import latlon
import gsw
import cftime
print("Download Temp")

institution_id=sys.argv[1]
source_id=sys.argv[2]
expt_id=sys.argv[3]
variant_id=sys.argv[4]
iteration_number=int(sys.argv[5])
print(institution_id,source_id,expt_id,variant_id,iteration_number)

if source_id != "MRI-ESM2-0":
	thetao_set=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","thetao")
else:
	thetao_set=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","thetao",'gr')

thetao_array=thetao_set.get("thetao")[iteration_number*12:(iteration_number+1)*12]
thetao=(thetao_array.values).astype(np.float32)

print("Download Salinity")
"""
if source_id!="MRI-ESM2-0":
	SO=xr.open_dataset("/badc/mo/data/CMIP6/CMIP/"+institution_id+"/"+source_id+"/"+expt_id+"/"+variant_id+"/Omon/so/gn/latest/so_Omon_"+source_id+"_"+expt_id+"_"+variant_id+"_gn_"+filename[-16:])
else:
	SO=xr.open_dataset("/badc/mo/data/CMIP6/CMIP/"+institution_id+"/"+source_id+"/"+expt_id+"/"+variant_id+"/Omon/so/gr/latest/so_Omon_"+source_id+"_"+expt_id+"_"+variant_id+"_gr_"+filename[-16:])
"""
if source_id != "MRI-ESM2-0":
	SO=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","so")
else:
	SO=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","so",'gr')
so=(SO.get('so')[iteration_number*12: (iteration_number+1)*12].values).astype(np.float32)

if "rho" in thetao_set.coords:
	rho=thetao_set.get('rho').values
	Density=np.tile(np.reshape(rho,(1,np.shape(rho)[0],1,1)),(np.shape(thetao)[0],1,np.shape(thetao)[2],np.shape(thetao)[3]))
	if np.nanmean(Density)>1000:
		Density=Density-1000
else:

	print("Download other stuff")
	if "lev" in thetao_set.coords:
		z=-thetao_set.get('lev').values
	elif "z" in thetao_set.coords:
		z=-thetao_set.get('z').values
	elif "olevel" in thetao_set.coords:
		z=-thetao_set.get('olevel').values
	if "latitude" in thetao_set.coords:
		latitude=thetao_set.get('latitude').values
	elif "lat" in thetao_set.coords:
		latitude=thetao_set.get('lat').values
	elif "j" in thetao_set.coords:
		latitude=thetao_set.get('j').values
	elif "nav_lat" in thetao_set.coords:
		latitude=thetao_set.get('nav_lat').values
	elif "y" in thetao_set.coords:
		latitude=thetao_set.get('y').values
	if "longitude" in thetao_set.coords:
		longitude=thetao_set.get("longitude").values
	elif "lon" in thetao_set.coords:
		longitude=thetao_set.get("lon").values
	elif "i" in thetao_set.coords:
		longitude=thetao_set.get("i").values
	elif "nav_lon" in thetao_set.coords:
		longitude=thetao_set.get("nav_lon").values
	elif "x" in thetao_set.coords:
		longitude=thetao_set.get("x").values


	if latitude.ndim==1 and longitude.ndim==1:
		latitude=np.tile(np.reshape(latitude,(len(latitude),1)),(1,len(longitude)))
		longitude=np.tile(np.reshape(longitude,(1,len(longitude))),(len(latitude),1))

	print("Calculate things")
	print(np.shape(z),np.shape(latitude))
	z_tiled=np.tile(np.reshape(z,(np.shape(z)[0],1,1)),(1,np.shape(latitude)[0],np.shape(latitude)[1]))
	latitude_tiled=np.tile(np.reshape(latitude,(1,np.shape(latitude)[0],np.shape(latitude)[1])),(np.shape(z)[0],1,1))
	longitude_tiled=np.tile(np.reshape(longitude,(1,np.shape(latitude)[0],np.shape(latitude)[1])),(np.shape(z)[0],1,1))


	pressure=gsw.conversions.p_from_z(z_tiled,latitude_tiled)
	pressure_full_tile=np.tile(np.reshape(pressure,(1,np.shape(z)[0],np.shape(latitude)[0],np.shape(latitude)[1])),(np.shape(so)[0],1,1,1))

	longitude_full_tile=np.tile(np.reshape(longitude_tiled,(1,np.shape(z)[0],np.shape(latitude)[0],np.shape(latitude)[1])),(np.shape(so)[0],1,1,1))
	latitude_full_tile=np.tile(np.reshape(latitude_tiled,(1,np.shape(z)[0],np.shape(latitude)[0],np.shape(latitude)[1])),(np.shape(so)[0],1,1,1))



	SA=gsw.SA_from_SP(so,pressure_full_tile,longitude_full_tile,latitude_full_tile)
	CT=gsw.CT_from_pt(SA,thetao)

	Density=gsw.density.sigma2(SA,CT)

if "time" in thetao_array.coords:
	time_coord=thetao_array.coords['time'].values
if "lev" in thetao_array.coords and (thetao_array.coords['lev'].values).ndim==1:
	lev_coord=thetao_array.coords['lev'].values
elif "z" in thetao_array.coords and (thetao_array.coords['z'].values).ndim==1:
	lev_coord=thetao_array.coords['z'].values
elif "olevel" in thetao_array.coords and (thetao_array.coords['olevel'].values).ndim==1:
        lev_coord=thetao_array.coords['olevel'].values
elif "rho" in thetao_array.coords and (thetao_array.coords['rho'].values).ndim==1:
        lev_coord=thetao_array.coords['rho'].values
if "j" in thetao_array.coords and (thetao_array.coords['j'].values).ndim==1:
	j_coord=thetao_array.coords['j'].values
elif "lat" in thetao_array.coords and (thetao_array.coords['lat'].values).ndim==1:
	j_coord=thetao_array.coords['lat'].values
elif "lat" in thetao_array.coords and (thetao_array.coords['lat'].values).ndim==2:
        j_coord=(["j","i"],thetao_array.coords['lat'].values)
elif "latitude" in thetao_array.coords and (thetao_array.coords['latitude'].values).ndim==1:
        j_coord=thetao_array.coords['latitude'].values
elif "nav_lat" in thetao_array.coords and (thetao_array.coords['nav_lat'].values).ndim==1:
        j_coord=thetao_array.coords['nav_lat'].values
elif "nav_lat" in thetao_array.coords and (thetao_array.coords['nav_lat'].values).ndim==2:
        j_coord=(["j","i"],thetao_array.coords['nav_lat'].values)
elif "y" in thetao_array.coords and (thetao_array.coords['y'].values).ndim==1:
        j_coord=thetao_array.coords['y'].values
if "i" in thetao_array.coords and (thetao_array.coords['i'].values).ndim==1:
	i_coord=thetao_array.coords['i'].values
elif "lon" in thetao_array.coords and (thetao_array.coords["lon"].values).ndim==1:
	i_coord=thetao_array.coords["lon"].values
elif "lon" in thetao_array.coords and (thetao_array.coords["lon"].values).ndim==2:
        i_coord=(["j","i"],thetao_array.coords["lon"].values)
elif "longitude" in thetao_array.coords and (thetao_array.coords["longitude"].values).ndim==1:
        i_coord=thetao_array.coords["longitude"].values
elif "nav_lon" in thetao_array.coords and (thetao_array.coords['nav_lon'].values).ndim==1:
        i_coord=thetao_array.coords["nav_lon"].values
elif "nav_lon" in thetao_array.coords and (thetao_array.coords['nav_lon'].values).ndim==2:
        i_coord=(["j","i"],thetao_array.coords['nav_lon'].values)
elif "x" in thetao_array.coords and (thetao_array.coords["x"].values).ndim==1:
        i_coord=thetao_array.coords["x"].values

if "lat" in thetao_array.coords and (thetao_array.coords['lat'].values).ndim==2:
        coords={'time':time_coord,'lev':lev_coord,'lat':j_coord,'lon':i_coord}
elif "nav_lat" in thetao_array.coords and (thetao_array.coords['nav_lat'].values).ndim==2:
        coords={'time':time_coord,'lev':lev_coord,'lat':j_coord,'lon':i_coord}
else:
        coords={'time':time_coord,'lev':lev_coord,'j':j_coord,'i':i_coord}


#coords=SO.coords


if "time" in thetao_set.dims:
        time_dim=thetao_set.dims['time']
if "lev" in thetao_set.dims:
        lev_dim=thetao_set.dims['lev']
elif "z" in thetao_set.coords:
	lev_dim=thetao_set.dims['z']
elif "olevel" in thetao_set.dims:
        lev_dim=thetao_set.dims['olevel']
elif "rho" in thetao_set.dims:
        lev_dim=thetao_set.dims['rho']
if "j" in thetao_set.dims:
        j_dim=thetao_set.dims['j']
elif "lat" in thetao_set.dims:
	j_dim=thetao_set.dims["lat"]
elif "latitude" in thetao_set.dims:
        j_dim=thetao_set.dims["latitude"]
elif "y" in thetao_set.dims:
	j_dim=thetao_set.dims["y"]
elif "nav_lat" in thetao_set.dims:
        j_dim=thetao_set.dims["nav_lat"]
if "i" in thetao_set.dims:
        i_dim=thetao_set.dims['i']
elif "lon" in thetao_set.dims:
	i_dim=thetao_set.dims["lon"]
elif "longitude" in thetao_set.dims:
        i_dim=thetao_set.dims["longitude"]
elif "x" in thetao_set.dims:
	i_dim=thetao_set.dims["x"]
elif "nav_lon" in thetao_set.dims:
        i_dim=thetao_set.dims["nav_lon"]




dims={'time':time_dim,'lev':lev_dim,'j':j_dim,'i':i_dim}

density_array=xr.DataArray(Density,dims=dims,coords=coords)

data_path="/gws/nopw/j04/orchestra_vol2/jonros74/Data_Improved/"

var_description="This is the potential density anomaly in kg/m^3 referenced to 2000 dbar."

if type(thetao_array.time.values[0])==cftime._cftime.Datetime360Day or type(thetao_array.time.values[0])==cftime._cftime.DatetimeNoLeap or type(thetao_array.time.values[0])==cftime._cftime.DatetimeProlepticGregorian or type(thetao_array.time.values[0])==cftime._cftime.DatetimeGregorian:
	years=str(thetao_array.time.values[0].year)+"-"+str(thetao_array.time.values[-1].year)
elif type(thetao_array.time.values[0])==np.datetime64:
	years=np.datetime_as_string(thetao_array.time.values[0])[:4]+"-"+np.datetime_as_string(thetao_array.time.values[-1])[:4]
else:
	years=str(thetao_array.time.values[0])+"-"+str(thetao_array.time.values[-1])
print(years)
jon_data.save(data_array=density_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="density2",var_long_name="Potential Density referenced to 2000 dbar",var_description=var_description,units="kg/m^3",freq="mon",spatial="glo",years=years)





