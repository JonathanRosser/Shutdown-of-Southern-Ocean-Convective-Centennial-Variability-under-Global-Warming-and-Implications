import xarray as xr
import numpy as np
import sys
sys.path.append('/home/users/jonros74/Coding/')
from JonTools import jon_data
from JonTools import latlon
import datetime
import cftime
from xhistogram.xarray import histogram
import gsw


#Define the model in question and the relevant variable, set up the script parameters
institution_id=sys.argv[1]
source_id=sys.argv[2]
expt_id=sys.argv[3]
variant_id=sys.argv[4]
iteration_number=int(sys.argv[5])
print(institution_id,source_id,expt_id,variant_id,iteration_number)

earth_radius=6371000
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



#if source_id != "MRI-ESM2-0":
thetao_set=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","thetao")
#else:
#        thetao_set=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","thetao",'gr')

thetao_array=thetao_set.get("thetao")[iteration_number*12:(iteration_number+1)*12]
thetao=(thetao_array.values).astype(np.float32)

#if source_id != "MRI-ESM2-0":
SO=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","so")
#else:
#        SO=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","so",'gr')
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

density_dims={'time':time_dim,'lev':lev_dim,'j':j_dim,'i':i_dim}

density_array=xr.DataArray(Density,dims=density_dims,coords=coords)
density_array=density_array.rename("density2")
density_values=Density










lev_bnds=jon_data.var_get(thetao_set,"lev_bnds")


if jon_data.mo_check(institution_id,source_id,expt_id,variant_id,"Omon","vmo")[1]==1:
	vmo_set=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","vmo")
	vmo_array=vmo_set.get("vmo")[iteration_number*12:(iteration_number+1)*12]
	#vmo=vmo_array.values
elif jon_data.mo_check(institution_id,source_id,expt_id,variant_id,"Omon","vo")[1]==1:
	vo_set=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","vo")
	vo_array=vo_set.get("vo")[iteration_number*12:(iteration_number+1)*12]
	vo=vo_array.values


	if np.ndim(lev_bnds)==3:
		height=lev_bnds[:,:,1]-lev_bnds[:,:,0]
		height_tile=np.tile(np.reshape(height[iteration_number*12:(iteration_number+1)*12,:],(12,np.shape(height)[1],1,1)),(1,1,np.shape(thetao)[2],np.shape(thetao)[3]))
	elif np.ndim(lev_bnds)==2:
		height=lev_bnds[:,1]-lev_bnds[:,0]
		height_tile=np.tile(np.reshape(height,(1,np.shape(height)[0],1,1)),(np.shape(thetao)[0],1,np.shape(thetao)[2],np.shape(thetao)[3]))

	lon_bnds=jon_data.var_get(thetao_set,"lon_bnds")
	if np.ndim(lon_bnds)==2:
		width=np.arccos((np.sin(-30*np.pi/180))**2+(np.cos(-30*np.pi/180))**2*np.cos(lon_bnds[:,1]-lon_bnds[:,0]))*earth_radius
		width_tile=np.tile(np.reshape(width,(1,1,np.shape(width)[0],1)),(np.shape(vo)[0],np.shape(vo)[1],1,np.shape(vo)[3]))
	elif np.ndim(lon_bnds)==3 and np.shape(lon_bnds)[0]==np.shape(vo)[2]:
		width=np.arccos((np.sin(-30*np.pi/180))**2+(np.cos(-30*np.pi/180))**2*np.cos(np.max(lon_bnds,axis=2)-np.min(lon_bnds,axis=2)))*earth_radius
		width_tile=np.tile(np.reshape(width,(1,1,np.shape(width)[0],np.shape(width)[1])),(np.shape(vo)[0],np.shape(vo)[1],1,1))
	elif np.ndim(lon_bnds)==3:
		width=np.arccos((np.sin(-30*np.pi/180))**2+(np.cos(-30*np.pi/180))**2*np.cos(np.max(lon_bnds,axis=2)-np.min(lon_bnds,axis=2)))*earth_radius
		width_tile=np.tile(np.reshape(width[iteration_number*12:(iteration_number+1)*12],(12,1,1,np.shape(width)[1])),(1,np.shape(vo)[1],np.shape(vo)[2],1))
	elif np.ndim(lon_bnds)==4:
		width=np.arccos((np.sin(-30*np.pi/180))**2+(np.cos(-30*np.pi/180))**2*np.cos(np.max(lon_bnds[iteration_number*12:(iteration_number+1)*12,:,:,:],axis=3)-np.min(lon_bnds[iteration_number*12:(iteration_number+1)*12,:,:,:],axis=3)))*earth_radius
		width_tile=np.tile(np.reshape(width,(np.shape(width)[0],1,np.shape(width)[1],np.shape(width)[2])),(1,np.shape(vo)[1],1,1))
	vmo=vo*height_tile*density_values*width_tile


	if "time" in thetao_set.coords:
		time_coord=thetao_array.coords['time'].values
	if "lev" in thetao_set.coords and (thetao_set.coords['lev'].values).ndim==1:
		lev_coord=thetao_set.coords['lev'].values
	elif "z" in thetao_set.coords and (thetao_set.coords['z'].values).ndim==1:
		lev_coord=thetao_set.coords['z'].values
	elif "olevel" in thetao_set.coords and (thetao_set.coords['olevel'].values).ndim==1:
		lev_coord=thetao_set.coords['olevel'].values
	elif "rho" in thetao_set.coords and (thetao_set.coords['rho'].values).ndim==1:
		lev_coord=thetao_set.coords['rho'].values
	if "j" in thetao_set.coords and (thetao_set.coords['j'].values).ndim==1:
		j_coord=thetao_set.coords['j'].values
	elif "lat" in thetao_set.coords and (thetao_set.coords['lat'].values).ndim==1:
		j_coord=thetao_set.coords['lat'].values
	elif "lat" in thetao_set.coords and (thetao_set.coords['lat'].values).ndim==2:
		j_coord=(["j","i"],thetao_set.coords['lat'].values)
	elif "latitude" in thetao_set.coords and (thetao_set.coords['latitude'].values).ndim==1:
		j_coord=thetao_set.coords['latitude'].values
	elif "nav_lat" in thetao_set.coords and (thetao_set.coords['nav_lat'].values).ndim==1:
		j_coord=thetao_set.coords['nav_lat'].values
	elif "nav_lat" in thetao_set.coords and (thetao_set.coords['nav_lat'].values).ndim==2:
		j_coord=(["j","i"],thetao_set.coords['nav_lat'].values)
	elif "y" in thetao_set.coords and (thetao_set.coords['y'].values).ndim==1:
		j_coord=thetao_set.coords['y'].values
	if "i" in thetao_set.coords and (thetao_set.coords['i'].values).ndim==1:
		i_coord=thetao_set.coords['i'].values
	elif "lon" in thetao_set.coords and (thetao_set.coords["lon"].values).ndim==1:
		i_coord=thetao_set.coords["lon"].values
	elif "lon" in thetao_set.coords and (thetao_set.coords["lon"].values).ndim==2:
		i_coord=(["j","i"],thetao_set.coords["lon"].values)
	elif "longitude" in thetao_set.coords and (thetao_set.coords["longitude"].values).ndim==1:
		i_coord=thetao_set.coords["longitude"].values
	elif "nav_lon" in thetao_set.coords and (thetao_set.coords['nav_lon'].values).ndim==1:
		i_coord=thetao_set.coords["nav_lon"].values
	elif "nav_lon" in thetao_set.coords and (thetao_set.coords['nav_lon'].values).ndim==2:
		i_coord=(["j","i"],thetao_set.coords['nav_lon'].values)
	elif "x" in thetao_set.coords and (thetao_set.coords["x"].values).ndim==1:
		i_coord=thetao_set.coords["x"].values

	if "lat" in thetao_set.coords and (thetao_set.coords['lat'].values).ndim==2:
		coords={'time':time_coord,'lev':lev_coord,'lat':j_coord,'lon':i_coord}
	elif "nav_lat" in thetao_set.coords and (thetao_set.coords['nav_lat'].values).ndim==2:
		coords={'time':time_coord,'lev':lev_coord,'lat':j_coord,'lon':i_coord}
	else:
		coords={'time':time_coord,'lev':lev_coord,'j':j_coord,'i':i_coord}

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




	vmo_array=xr.DataArray(vmo,dims=dims,coords=coords,name="vmo")

if institution_id=="NCC":
        binval=np.arange(np.nanmin(density_array.density2.values),np.nanmax(density_array.density2.values),0.01)
else:
        binval=np.append(np.append(np.arange(20,34.5,0.1),np.arange(34.5,38,0.001)),np.arange(38,42,0.1))
midbin=(binval[:-1]+binval[1:])/2

lat=jon_data.coord_get(thetao_set,"latitude")
if np.ndim(lat)==2:
        lat=np.nanmean(lat,axis=1)


if vmo_array.shape[2]==density_array.shape[2]:
	vmo_array.fillna(0)
	vmo_array=vmo_array.rename({vmo_array.dims[0]:density_array.dims[0],vmo_array.dims[1]:density_array.dims[1],vmo_array.dims[2]:density_array.dims[2],vmo_array.dims[3]:density_array.dims[3]})

	vmo_array.coords["j"]=density_array.coords["j"]
	vmo_array.coords["i"]=density_array.coords["i"]

	vmo_mask=np.isfinite(vmo_array[0,:,:,:])
elif abs(vmo_array.shape[2]-density_array.shape[2])<3:
	vmo_array.fillna(0)
	vmo_array=vmo_array.rename({vmo_array.dims[0]:density_array.dims[0],vmo_array.dims[1]:density_array.dims[1],vmo_array.dims[2]:density_array.dims[2],vmo_array.dims[3]:density_array.dims[3]})
	if density_array.shape[2] >vmo_array.shape[2]:
		lat=lat[:-(density_array.shape[2]-vmo_array.shape[2])]
		vmo_array.coords["j"]=density_array.coords["j"][:-(density_array.shape[2]-vmo_array.shape[2])]
		density_array=density_array[:,:,:-(density_array.shape[2]-vmo_array.shape[2]),:]
	vmo_array.coords["i"]=density_array.coords["i"]
	vmo_mask=np.isfinite(vmo_array[0,:,:,:])




vmosum=histogram(density_array.where(vmo_mask==1),bins=[binval],weights=(vmo_array),dim=['lev','i'])

overcirc=vmosum.cumsum(dim="density2_bin",skipna=True)
streamrhon_array=overcirc.rename("streamrhon2")

streamrhon=streamrhon_array
streamrhon=streamrhon.assign_coords({"lat":("j",lat)})


max_upper_density_value=38
max_lower_density_value=34.5
max_upper_lat_value=-19
max_lower_lat_value=-90

min_upper_density_value=50
min_lower_density_value=36.5
min_upper_lat_value=0
min_lower_lat_value=-90



Max=(streamrhon.where((streamrhon.lat<max_upper_lat_value)*(streamrhon.lat>max_lower_lat_value)*(streamrhon.density2_bin<max_upper_density_value)*(streamrhon.density2_bin>max_lower_density_value))).max(dim=('j','density2_bin'), skipna=True).values
Min=(streamrhon.where((streamrhon.lat<min_upper_lat_value)*(streamrhon.lat>min_lower_lat_value)*(streamrhon.density2_bin<min_upper_density_value)*(streamrhon.density2_bin>min_lower_density_value))).min(dim=('j','density2_bin'), skipna=True).values

data_path="/gws/nopw/j04/orchestra_vol2/jonros74/Data_Improved/"


max_array=xr.DataArray(Max,dims=('time'),coords={'time':streamrhon_array.coords['time']},name='uppercircrhon')
min_array=xr.DataArray(Min,dims=('time'),coords={'time':streamrhon_array.coords['time']},name='lowercircrhon')


max_description="This is the Upper Meridional Circulation calculated as the max of the mass streamfunction in sigma2 coordinates south of a 19S and within specific density bounds."

min_description="This is the Lower Meridional Circulation calculated as the min of the mass streamfunction in sigma2 coordinates."

if type(thetao_array.time.values[0])==cftime._cftime.Datetime360Day or type(thetao_array.time.values[0])==cftime._cftime.DatetimeNoLeap or type(thetao_array.time.values[0])==cftime._cftime.DatetimeProlepticGregorian or type(thetao_array.time.values[0])==cftime._cftime.DatetimeGregorian:
        years=str(thetao_array.time.values[0].year)+"-"+str(thetao_array.time.values[-1].year)
elif type(thetao_array.time.values[0])==np.datetime64:
        years=np.datetime_as_string(thetao_array.time.values[0])[:4]+"-"+np.datetime_as_string(thetao_array.time.values[-1])[:4]
else:
        years=str(thetao_array.time.values[0])+"-"+str(thetao_array.time.values[-1])
print(years)




jon_data.save(data_array=max_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="uppercircrhon2",var_long_name="Upper Meridional Mass Circulation in Sigma2 Space", var_description=max_description,units="kgs^(-1)",freq="mon",spatial="sin",years=years)


jon_data.save(data_array=min_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="lowercircrhon2",var_long_name="Lower Meridional Mass Circulation in Sigma2 Space", var_description=min_description,units="kgs^(-1)",freq="mon",spatial="sin",years=years)




