import xarray as xr
import numpy as np
import sys
sys.path.append('/home/users/jonros74/Coding/')
from JonTools import jon_data
from JonTools import latlon
import gsw
import cftime
print("Download Temp")



def find_indices(X,threshold):
    #This function will find the first indices greater than the threshold
    shape=np.shape(X)
    index=np.zeros((shape[0],shape[2],shape[3]))
    for i in range(0,shape[0]):
        for j in range(0,shape[2]):
            for k in range(0,shape[3]):
                Val=np.where(X[i,:,j,k]>threshold)
                if len(Val[0])>0:
                    index[i,j,k]=Val[0][0]
                elif np.isnan(X[i,0,j,k])==False:
                    index[i,j,k]=np.where(np.isnan(X[i,:,j,k])==False)[0][-1]
                elif np.isnan(X[i,0,j,k])==True:
                    index[i,j,k]=0
                else:
                    print("error",i,j,k)
    return index

data_path="/gws/nopw/j04/orchestra_vol2/jonros74/Data_Improved/"


institution_id=sys.argv[1]
source_id=sys.argv[2]
expt_id=sys.argv[3]
variant_id=sys.argv[4]
iteration_number=int(sys.argv[5])
print(institution_id,source_id,expt_id,variant_id,iteration_number)

if source_id=="CNRM-CM6-1":
        areacello=jon_data.cmip6_load(institution_id,source_id,"piControl","r1i1p1f2","Ofx","areacello").areacello.values
elif source_id=="CanESM5":
        areacello=jon_data.cmip6_load(institution_id,source_id,"esm-piControl","r1i1p1f1","Ofx","areacello").areacello.values
else:
        areacello=jon_data.cmip6_load(institution_id,source_id,"piControl","r1i1p1f1","Ofx","areacello").areacello.values



if source_id != "MRI-ESM2-0":
	thetao_set=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","thetao")
else:
	thetao_set=jon_data.mo_load(institution_id,source_id,expt_id,variant_id,"Omon","thetao",'gr')

thetao_array=thetao_set.get("thetao")[iteration_number*12:(iteration_number+1)*12]
thetao=(thetao_array.values).astype(np.float32)

print("Download Salinity")
"""
if source_id!="MRI-ESM2-0":
	SO=xr.open_dataset("/badc/cmip6/data/CMIP6/CMIP/"+institution_id+"/"+source_id+"/"+expt_id+"/"+variant_id+"/Omon/so/gn/latest/so_Omon_"+source_id+"_"+expt_id+"_"+variant_id+"_gn_"+filename[-16:])
else:
	SO=xr.open_dataset("/badc/cmip6/data/CMIP6/CMIP/"+institution_id+"/"+source_id+"/"+expt_id+"/"+variant_id+"/Omon/so/gr/latest/so_Omon_"+source_id+"_"+expt_id+"_"+variant_id+"_gr_"+filename[-16:])
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

	Density=gsw.density.sigma0(SA,CT)

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

density_values=Density

density_shape=np.shape(density_values)
MLD001=np.zeros((density_shape[0],density_shape[2],density_shape[3]))
MLD003=np.zeros((density_shape[0],density_shape[2],density_shape[3]))
Diff=density_values-np.tile(np.reshape(density_values[:,0,:,:],(density_shape[0],1,density_shape[2],density_shape[3])),(1,density_shape[1],1,1))
Diff001=find_indices(Diff,0.01)
Diff003=find_indices(Diff,0.03)
shape=np.shape(Diff001)
for i in range(0,shape[0]):
	for j in range(0,shape[1]):
		for k in range(0,shape[2]):
			MLD001[i,j,k]=abs(z[int(Diff001[i,j,k])])
			MLD003[i,j,k]=abs(z[int(Diff003[i,j,k])])
nan_mask=density_values[:,0,:,:]*0+1


if type(thetao_array.time.values[0])==cftime._cftime.Datetime360Day or type(thetao_array.time.values[0])==cftime._cftime.DatetimeNoLeap or type(thetao_array.time.values[0])==cftime._cftime.DatetimeProlepticGregorian or type(thetao_array.time.values[0])==cftime._cftime.DatetimeGregorian:
        years=str(thetao_array.time.values[0].year)+"-"+str(thetao_array.time.values[-1].year)
elif type(thetao_array.time.values[0])==np.datetime64:
        years=np.datetime_as_string(thetao_array.time.values[0])[:4]+"-"+np.datetime_as_string(thetao_array.time.values[-1])[:4]
else:
        years=str(thetao_array.time.values[0])+"-"+str(thetao_array.time.values[-1])
print(years)

##MLD Below 50S
area_mask=latlon.area(thetao_set,maxlat=-50)
mld_weighted=MLD003*nan_mask*areacello


avg_mld=np.nansum(mld_weighted*area_mask,axis=(1,2))/np.nansum(areacello*area_mask)

avgmld_array=xr.DataArray(avg_mld,dims=('time'),coords={'time':time_coord},name='avgmldd0')

avgmld_description='The average Mixed Layer Depth using a 0.03kgm^(-3) criterion using sigma0, south of 50S.'


jon_data.save(data_array=avgmld_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="avgmldd0",var_long_name="Average Mixed Layer Depth south of 50S with criterion 0.03kgm^(-3) using sigma0",var_description=avgmld_description,units="m",freq="mon",spatial="sin",years=years)


Rossmask=latlon.area(thetao_set,maxlat=-60,minlat=-75,minlon=175)+latlon.area(thetao_set,maxlat=-60,minlat=-75,maxlon=-125)
Weddellmask=latlon.area(thetao_set,maxlat=-60,minlat=-73,maxlon=5,minlon=-62.5)



r_avgmld=np.nansum(mld_weighted*Rossmask,axis=(1,2))/np.nansum(areacello*Rossmask)

r_avgmld_array=xr.DataArray(r_avgmld,dims=('time'),coords={'time':time_coord},name='r_avgmldd0')

r_avgmld_description='The average Mixed Layer Depth using a 0.03kgm^(-3) criterion, in the Ross sea using sigma0.'


jon_data.save(data_array=r_avgmld_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="r_avgmldd0",var_long_name="Average Mixed Layer Depth in the Ross with criterion 0.03kgm^(-3) using sigma0",var_description=r_avgmld_description,units="m",freq="mon",spatial="sin",years=years)

w_avgmld=np.nansum(mld_weighted*Weddellmask,axis=(1,2))/np.nansum(areacello*Weddellmask)

w_avgmld_array=xr.DataArray(w_avgmld,dims=('time'),coords={'time':time_coord},name='w_avgmldd0')

w_avgmld_description='The average Mixed Layer Depth using a 0.03kgm^(-3) criterion, in the Weddell sea using sigma0.'


jon_data.save(data_array=w_avgmld_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="w_avgmldd0",var_long_name="Average Mixed Layer Depth in the Weddell with criterion 0.03kgm^(-3) using sigma0",var_description=w_avgmld_description,units="m",freq="mon",spatial="sin",years=years)


maxmld_description="Maximum Mixed Layer Depth south of 50S with criterion 0.03kgm^(-3) using sigma0"

maxmld=np.nanmax(MLD003*area_mask,axis=(1,2))

maxmld_array=xr.DataArray(maxmld,dims=('time'),coords={'time':time_coord},name='maxmldd0')

jon_data.save(data_array=maxmld_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="maxmldd0",var_long_name="Maximum Mixed Layer Depth south of 50S with criterion 0.03kgm^(-3) using sigma0",var_description=maxmld_description,units="m",freq="mon",spatial="sin",years=years)

w_maxmld_description="Maximum Mixed Layer Depth in the Weddell with criterion 0.03kgm^(-3) using sigma0"

w_maxmld=np.nanmax(MLD003*Weddellmask,axis=(1,2))

w_maxmld_array=xr.DataArray(w_maxmld,dims=('time'),coords={'time':time_coord},name='w_maxmldd0')

jon_data.save(data_array=w_maxmld_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="w_maxmldd0",var_long_name="Maximum Mixed Layer Depth in the Weddell with criterion 0.03kgm^(-3) using sigma0",var_description=w_maxmld_description,units="m",freq="mon",spatial="sin",years=years)


r_maxmld_description="Maximum Mixed Layer Depth in the Ross with criterion 0.03kgm^(-3) using sigma0"

r_maxmld=np.nanmax(MLD003*Rossmask,axis=(1,2))

r_maxmld_array=xr.DataArray(r_maxmld,dims=('time'),coords={'time':time_coord},name='r_maxmldd0')

jon_data.save(data_array=r_maxmld_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="r_maxmldd0",var_long_name="Maximum Mixed Layer Depth in the Ross with criterion 0.03kgm^(-3) using sigma0",var_description=r_maxmld_description,units="m",freq="mon",spatial="sin",years=years)

Arcticmask=latlon.area(thetao_set,maxlat=90,minlat=50,maxlon=40,minlon=-40)


a_maxmld_description="Maximum Mixed Layer Depth in the Arctic with criterion 0.03kgm^(-3) using sigma0"

a_maxmld=np.nanmax(MLD003*Arcticmask,axis=(1,2))

a_maxmld_array=xr.DataArray(a_maxmld,dims=('time'),coords={'time':time_coord},name='a_maxmldd0')

jon_data.save(data_array=a_maxmld_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="a_maxmldd0",var_long_name="Maximum Mixed Layer Depth in the Arctic with criterion 0.03kgm^(-3) using sigma0",var_description=a_maxmld_description,units="m",freq="mon",spatial="sin",years=years)

Labradormask=latlon.area(thetao_set,maxlat=68,minlat=50,maxlon=-40,minlon=-65)


l_maxmld_description="Maximum Mixed Layer Depth in the Labrador sea with criterion 0.03kgm^(-3) using sigma0"

l_maxmld=np.nanmax(MLD003*Labradormask,axis=(1,2))

l_maxmld_array=xr.DataArray(l_maxmld,dims=('time'),coords={'time':time_coord},name='l_maxmldd0')

jon_data.save(data_array=l_maxmld_array,data_path=data_path,source1=source_id,source2=expt_id,source3=variant_id,rpa="R",var_name="l_maxmldd0",var_long_name="Maximum Mixed Layer Depth in the Labrador sea with criterion 0.03kgm^(-3) using sigma0",var_description=l_maxmld_description,units="m",freq="mon",spatial="sin",years=years)








