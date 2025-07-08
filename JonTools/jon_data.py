import xarray as xr
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
import sys
from datetime import date
import pickle
import glob
from scipy.stats import pearsonr


def save(data_array, data_path,source1,rpa,var_name,var_long_name,var_description,units,freq,spatial,years=None,type_analysis=None,params1=None,params2=None,params3=None,source2=None,source3=None,misc=None):

        if source2==None:
            source_path=source1
            source_name=source1+"_"
        elif source2 !=None and source3==None:
            source_path=source1+"/"+source2
            source_name=source1+"_"+source2+"_"
        elif source3 != None:
            source_path=source1+"/"+source2+"/"+source3
            source_name=source1+"_"+source2+"_"+source3+"_"
        else:
            raise NameError('Source not found or poorly defined')

        if params1==None:
            params=""
        elif params1!=None and params2==None:
            params=params1+"_"
        elif params2!=None and params3==None:
            params=params1+"_"+params2+"_"
        elif params3!=None:
            params=params1+"_"+params2+"_"+params3+"_"
        else:
            raise NameError('Params not found or poorly defined')

        if years==None:
            years_name=""
        elif years!=None:
            years_name=years
        else:
            raise NameError('Years not found or poorly defined')

        if type_analysis==None:
            type_analysis_name=""
        elif type_analysis!=None:
            type_analysis_name=type_analysis+"_"
        else:
            raise NameError('type of analysis not found or poorly defined')


        path=data_path+source_path+"/"+rpa+"/"+var_name+"/"
        file_name=var_name+"_"+rpa+"_"+type_analysis_name+freq+"_"+spatial+"_"+params+source_name+years_name+".nc"

        if not os.path.exists(path):
            os.makedirs(path)

        data_array.name=var_name
        data_array.attrs['long_name']=var_long_name
        data_array.attrs['var_name']=var_name
        data_array.attrs['rpa']=rpa
        data_array.attrs['description']=var_description
        data_array.attrs['units']=units
        data_array.attrs['freq']=freq
        data_array.attrs['spatial']=spatial

        data_array.attrs['source']=source_name
        data_array.attrs['prod_file']=sys.argv[0]
        today=date.today()
        data_array.attrs['date']=today.strftime("%d/%m/%Y")
        if params1!=None:
            data_array.attrs['params']=params
        if years!=None:
            data_array.attrs['years']=years
        if type_analysis!=None:
            data_array.attrs['type_analysis']=type_analysis
        if misc!=None:
            data_array.attrs['misc']=misc

	#Store a list of short variable names and sources
        '''if os.path.exists(data_path+"var_names.txt"):
                y=open(data_path+"var_names.txt","rb")
                var_name_file=pickle.load(y)
                if not var_name in var_name_file:
                        var_name_file.append(var_name)
                        y=open(data_path+"var_names.txt","wb")
                        pickle.dump(var_name_file,y)
        else:
                y=open(data_path+"var_names.txt","wb")		
                pickle.dump([var_name],y)

        if os.path.exists(data_path+"sources.txt"):
                y=open(data_path+"sources.txt","rb")
                source_name_file=pickle.load(y)
                if not source_name in source_name_file:
                        source_name_file.append(source_name)
                        y=open(data_path+"sources.txt","wb")
                        pickle.dump(source_name_file,y)
        else:
                y=open(data_path+"sources.txt","wb")

                pickle.dump([source_name],y)
	'''




        data_array.to_netcdf(path=path+file_name)

"""
def load(data_path,source_id,expt_id,variant_id,rpa,var_name,freq,spatial,years=None):
	source_name=source_id+"_"+expt_id+"_"+variant_id+"_"
	if years==None:
		X=xr.open_mfdataset(data_path+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_"+freq+"_"+spatial+"_"+source_name"*.nc")
	else:
		X=xr.open_dataset(data_path++source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_"+freq+"_"+spatial+"_"+source_name+years+".nc")
"""




def cmip6_load(institution_id,source_id,expt_id,variant_label,table_id,var_name):
	#Given the required CMIP6 data dimensions this will retrieve the given variable between the two years listed (inclusive)
	data_path="/badc/cmip6/data/CMIP6/CMIP/"
	version_location=data_path+institution_id+'/'+source_id+'/'+expt_id+'/'+variant_label+'/'+table_id+'/'+var_name+'/gn/'
	if os.path.exists(version_location)==False:
		print("File location does not exist")
		raise FileNotFoundError 
	version=os.listdir(version_location)[-1]
	if version[0]!='v':
		print("Variable is not downloaded")
		raise FileNotFoundError
	else:
		data_location=version_location+version+'/'
	files=os.listdir(data_location)
	if len(files)==0:
		print("No data for this variable")
		return FileNotFoundError
	X=xr.open_mfdataset(data_location+"*.nc",combine='by_coords',use_cftime=True)
	return X
		

def cmip6_years(institution_id,source_id,expt_id,variant_label,table_id,var_name):
        #Given the required CMIP6 data dimensions this will retrieve the given variable between the two years listed (inclusive)
        data_path="/badc/cmip6/data/CMIP6/CMIP/"
        data_location=data_path+institution_id+'/'+source_id+'/'+expt_id+'/'+variant_label+'/'+table_id+'/'+var_name+'/gn/latest/'
        files=os.listdir(data_location)	
        start_year=files[0][-16:-12]
        end_year=files[-1][-9:-5]
        years=str(start_year)+"-"+str(end_year)
        return years

def jasmin_check(institution_id,source_id,expt_id,variant_label,table_id,var_name):
        data_path="/badc/cmip6/data/CMIP6/CMIP/"
        version_location=data_path+institution_id+'/'+source_id+'/'+expt_id+'/'+variant_label+'/'+table_id+'/'+var_name+'/gn/'
        if os.path.exists(version_location)==False:
                return version_location+" Does not Exist",0
        version=os.listdir(version_location)[-1]
        if version[0]!='v':
                return "latest directory is not a version",0
        else:
                data_location=version_location+version+'/'
        files=os.listdir(data_location)
        if len(files)!=0:
                return data_location+" Contains Files",1




def var_get(X,variable):
        if variable=="lev_bnds":
                if "lev_bnds" in X.variables:
                        lev_bnds=X.get("lev_bnds").values
                elif "lev_bounds" in X.variables:
                        lev_bnds=X.get("lev_bounds").values
                elif "olevel_bounds" in X.variables:
                        lev_bnds=X.get("olevel_bounds").values
                return lev_bnds
        if variable=="lat_bnds":
                if "lat_bnds" in X.variables:
                        lat_bnds=X.get("lat_bnds").values
                elif "bounds_lat" in X.variables:
                        lat_bnds=X.get("bounds_lat").values
                elif "vertices_latitude" in X.variables:
                        lat_bnds=X.get("vertices_latitude").values
                elif "bounds_nav_lat" in X.variables:
                        lat_bnds=X.get("bounds_nav_lat").values
                return lat_bnds
        if variable=="lon_bnds":
                if "lon_bnds" in X.variables:
                        lon_bnds=X.get("lon_bnds").values
                elif "bounds_lon" in X.variables:
                        lon_bnds=X.get("bounds_lon").values
                elif "vertices_longitude" in X.variables:
                        lon_bnds=X.get("vertices_longitude").values
                elif "bounds_nav_lon" in X.variables:
                        lon_bnds=X.get("bounds_nav_lon").values
                return lon_bnds



def dim_get(X,variable):
	if variable=="lev_bnds":
		if "lev_bnds" in X.dims:
			lev_bnds=X.get("lev_bnds").values
		elif "lev_bounds" in X.dims:
			lev_bnds=X.get("lev_bounds").values
		return lev_bnds
	if variable=="lat_bnds":
		if "lat_bnds" in X.dims:
			lat_bnds=X.get("lat_bnds").values
		elif "bounds_lat" in X.dims:
			lat_bnds=X.get("bounds_lat").values
		return lat_bnds
	if variable=="lon_bnds":
		if "lon_bnds" in X.dims:
			lon_bnds=X.get("lon_bnds").values
		elif "bounds_lon" in X.dims:
			lon_bnds=X.get("bounds_lon").values
		return lon_bnds


def coord_get(X,variable):
	if variable=="longitude":
		if "longitude" in X.coords:
			longitude=X.get("longitude").values
			longitude=np.mod(longitude+180,360)-180
		elif "lon" in X.coords:
			longitude=X.get("lon").values
			longitude=np.mod(longitude+180,360)-180
		elif "i" in X.coords:
			longitude=X.get("i").values
			longitude=np.mod(longitude+180,360)-180
		elif "nav_lon" in X.coords:
			longitude=X.get("nav_lon").values
			longitude=np.mod(longitude+180,360)-180
		elif "x" in X.coords:
			longitude=X.get("x").values
			longitude=np.mod(longitude+180,360)-180

		else:
			print("No longitude to retrieve")
		
		return longitude
	elif variable=="latitude":
		if "latitude" in X.coords:
			latitude=X.get('latitude').values
		elif "lat" in X.coords:
			latitude=X.get('lat').values
		elif "j" in X.coords:
			latitude=X.get('j').values
		elif "nav_lat" in X.coords:
			latitude=X.get('nav_lat').values
		elif "y" in X.coords:
			latitude=X.get('y').values
		return latitude
	if variable=="z":
		if "lev" in X.coords:
			z=-X.get('lev').values
		elif "z" in X.coords:
			z=-X.get('z').values
		elif "olevel" in X.coords:
			z=-X.get('olevel').values
		return z



def ukesm_data_load(variable,ocean_atmos):
    #This function will load the CMIP6 picontrol data for the UKESM for a choice of atmosphere or oceand variable and it will combine the 100 years extracted
    raw_data=xr.open_mfdataset('/gws/nopw/j04/orchestra/CMIP6/piControl/{}/UKESM1-0-LL/r1i1p1f2/{}/gn/*.nc'.format(variable,ocean_atmos))
    data=(raw_data.get(variable)).values
    return data

#def CMIP6_Raw_Load(variable,table_id,source_id,exp_id,var_label,date_start,date_end):
    #This function will go to the UKESM data directly and create a dataset of the data of interest 
    

def deseason(X):
    K = X.astype('float64')
    Y=np.reshape(K,(12,int(len(K)/12)),order='F')
    D=np.mean(Y,axis=1)
    M=np.tile(np.reshape(D,(12,1)),(1,int(len(K)/12)))
    Diff=Y-M
    Result=np.reshape(Diff,np.shape(K),order='F')
    return Result

def detrend(X):
    K = X.astype('float64')
    Y=np.reshape(np.arange(len(K)),(len(K),1))
    model=LinearRegression()
    model.fit(Y,K)
    trend=model.predict(Y)
    detrended=K-trend
    return detrended

def standardise(X):
    K=X-np.nanmean(X)
    L=K/np.nanstd(K)
    return(L)


def time_average(X,period):
    D=len(X)/period
    if D.is_integer():
        Y=np.nanmean(np.reshape(X,(-1,period)),axis=1)
    else:
        remainder=len(X)%period
        Y=np.nanmean(np.reshape(X[:-remainder],(-1,period)),axis=1)
    return Y



def time_max(X,period):
    D=len(X)/period
    if D.is_integer():
        Y=np.nanmax(np.reshape(X,(-1,period)),axis=1)
    else:
        remainder=len(X)%period
        Y=np.nanmax(np.reshape(X[:-remainder],(-1,period)),axis=1)
    return Y

def run_average(X,period):
    Length=len(X)
    run_avg=np.zeros(Length-period)
    for j in range(0,Length-period):
        run_avg[j]=np.mean(X[j:j+period])
    return run_avg

def lag_corr(X,Y,lag):
    if lag>0:
        result=pearsonr(X[:-lag],Y[lag:])
    elif lag<0:
        result=pearsonr(X[abs(lag):],Y[:-abs(lag)])
    elif lag==0:
        result=pearsonr(X,Y)
    return result


def lag_corr_analysis(values,cvalues,max_lag):
    minlen=np.min((len(values),len(cvalues)))
    lag_corr_values=np.zeros((2*max_lag+1,2))
    minvalues=values[:minlen]
    mincvalues=cvalues[:minlen]
    for m in range(0,2*max_lag+1):
        lag_corr_values[m]=lag_corr(minvalues,mincvalues,m-max_lag)
    max_val=np.nanmax(lag_corr_values[:,0])
    min_val=np.nanmin(lag_corr_values[:,0])
    if max_val > -min_val:
        lag_corr_mag=max_val
        lag_position=np.where(lag_corr_values[:,0]==lag_corr_mag)[0]-max_lag
        lag_sig=lag_corr_values[np.where(lag_corr_values[:,0]==lag_corr_mag)[0],1]
    elif max_val < -min_val:
        lag_corr_mag=min_val
        lag_position=np.where(lag_corr_values[:,0]==lag_corr_mag)[0]-max_lag
        lag_sig=lag_corr_values[np.where(lag_corr_values[:,0]==lag_corr_mag)[0],1]
    else:
        lag_corr_mag=0
        lag_position=0
        lag_sig=1
    return lag_corr_mag,lag_position,lag_sig

def var_load(var_name,data_path,source_id,expt_id,variant_id,rpa,freq=None,spatial=None):
    Directory=data_path+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name
    source_name=source_id+"_"+expt_id+"_"+variant_id+"_"
    if os.path.exists(Directory)==False:
        print(Directory,"Does Not Exist")
    elif os.listdir(Directory)==[]:
        print(Directory,"Empty")
    elif rpa=="original":
        Y=xr.open_mfdataset(Directory+"/*.nc")
        return Y
    elif len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])==True:
        print(Directory,"Contains Files")
        print(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
        Y=xr.open_dataset(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
        return Y
    elif len(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
        Y=xr.open_mfdataset("/home/jonathan/Documents/Data/"+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc",combine="by_coords")
        return Y
    else:
         print(Directory,"None of the Above")



def lag_corr(X,Y,lag):
    if lag>0:
        result=pearsonr(X[:-lag],Y[lag:])
    elif lag<0:
        result=pearsonr(X[abs(lag):],Y[:-abs(lag)])
    elif lag==0:
        result=pearsonr(X,Y)
    return result


def lag_corr_analysis(values,cvalues,max_lag):
    minlen=np.min((len(values),len(cvalues)))
    lag_corr_values=np.zeros((2*max_lag+1,2))
    minvalues=values[:minlen]
    mincvalues=cvalues[:minlen]
    for m in range(0,2*max_lag+1):
        lag_corr_values[m]=lag_corr(minvalues,mincvalues,m-max_lag)
    max_val=np.nanmax(lag_corr_values[:,0])
    min_val=np.nanmin(lag_corr_values[:,0])
    if max_val > -min_val:
        lag_corr_mag=max_val
        lag_position=np.where(lag_corr_values[:,0]==lag_corr_mag)[0]-max_lag
        lag_sig=lag_corr_values[np.where(lag_corr_values[:,0]==lag_corr_mag)[0],1]
    elif max_val < -min_val:
        lag_corr_mag=min_val
        lag_position=np.where(lag_corr_values[:,0]==lag_corr_mag)[0]-max_lag
        lag_sig=lag_corr_values[np.where(lag_corr_values[:,0]==lag_corr_mag)[0],1]
    else:
        lag_corr_mag=0
        lag_position=0
        lag_sig=1
    return lag_corr_mag,lag_position,lag_sig

def var_load(var_name,data_path,source_id,expt_id,variant_id,rpa,freq=None,spatial=None):
    Directory=data_path+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name
    source_name=source_id+"_"+expt_id+"_"+variant_id+"_"
    if os.path.exists(Directory)==False:
        print(Directory,"Does Not Exist")
    elif os.listdir(Directory)==[]:
        print(Directory,"Empty")
    elif rpa=="original":
        Y=xr.open_mfdataset(Directory+"/*.nc")
        return Y
    elif len(glob.glob(data_path+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc"))!=0 and os.path.isfile(glob.glob(data_path+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])==True:
        print(Directory,"Contains Files")
        print(glob.glob(data_path+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
        Y=xr.open_dataset(glob.glob(data_path+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"_concat_"+freq+"_"+spatial+"_"+source_name+"*.nc")[0])
        return Y
    elif len(glob.glob(data_path+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc"))!=0 and os.path.isfile(glob.glob(data_path+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")[0])==True:
        Y=xr.open_mfdataset(data_path+source_id+"/"+expt_id+"/"+variant_id+"/"+rpa+"/"+var_name+"/"+var_name+"_"+rpa+"*.nc")
        return Y
    else:
         print(Directory,"None of the Above")









def jasmin_check(institution_id,source_id,expt_id,variant_label,table_id,var_name):
        data_path="/badc/cmip6/data/CMIP6/CMIP/"
        version_location=data_path+institution_id+'/'+source_id+'/'+expt_id+'/'+variant_label+'/'+table_id+'/'+var_name+'/gn/'
        if os.path.exists(version_location)==False:
                return version_location+" Does not Exist",0
        version=os.listdir(version_location)[-1]
        if version[0]!='v':
                return "latest directory is not a version",0
        else:
                data_location=version_location+version+'/'
        files=os.listdir(data_location)
        if len(files)!=0:
                return data_location+" Contains Files",1




def analysis1D(X,units,location,name,long_name):
    X=X.astype(np.float64)
    stats=np.zeros(4)
    stats[0]=np.mean(X)
    stats[1]=np.std(X)
    stats[2]=np.max(X)
    stats[3]=np.min(X)
    if not os.path.exists(location+name):
        os.makedirs(location+name)
    X_avg=np.mean(np.reshape(X,(int(len(X)/12),12)),axis=1)
    if not os.path.exists(location+name):
        os.makedirs(location+name)
    plt.close()
    plt.plot(X_avg)
    plt.ylabel(units)
    plt.xlabel('time(years)')
    plt.title("Annual Average of "+long_name)
    plt.tight_layout()
    plt.savefig(location+name+'/'+name+'_1D_Annual_plot.png')
    plt.close()
    decades=int(len(X)/120)
    X_decade_avg=np.mean(np.reshape(X[:int(decades*120)],(int(len(X[:int(decades*120)])/120),120)),axis=1)
    plt.plot(X_decade_avg)
    plt.ylabel(units)
    plt.xlabel('time(decades)')
    plt.title("Decadal Average of "+long_name)
    plt.tight_layout()
    plt.savefig(location+name+'/'+name+'_1D_Decadal_plot.png')
    plt.close()
    halfcenturies=int(len(X)/600)
    X_halfcentury_avg=np.mean(np.reshape(X[:int(halfcenturies*600)],(int(len(X[:int(halfcenturies*600)])/600),600)),axis=1)
    plt.plot(X_halfcentury_avg)
    plt.ylabel(units)
    plt.xlabel('time(half centuries)')
    plt.title("50 year average of "+long_name)
    plt.tight_layout()
    plt.savefig(location+name+'/'+name+'_1D_Half_Century_plot.png')
    #Calculate Running Averages
    avg_list=[120,600]
    for i in range(0,len(avg_list)):
        period=avg_list[i]
        Length=len(X)
        run_avg=np.zeros(Length-period)
        for j in range(0,Length-period):
            run_avg[j]=np.mean(X[j:j+period])
        plt.close()
        plt.plot(run_avg)
        plt.ylabel(units)
        plt.xlabel('time(months)')
        if period==120:
            plt.title("Decadal running average of "+long_name)
        elif period==600:
            plt.title("50 year running average of "+long_name)
        plt.tight_layout()
        plt.savefig(location+name+'/'+name+'_1D_Run_Avg_{}.png'.format(period))

    print(location+name+'/stats.npy')
    np.save(location+name+'/stats.npy',stats)
    plt.close()
    plt.plot(X)
    plt.ylabel(units)
    plt.xlabel('time(months)')
    plt.title(long_name)
    plt.tight_layout()
    plt.savefig(location+name+'/'+name+'_1D_plot.png')
    plt.close()

    plt.hist(X,bins=100)
    plt.ylabel('Frequency')
    plt.xlabel(units)
    plt.title("Histogram of "+long_name)
    plt.tight_layout()
    plt.savefig(location+name+'/'+name+'_hist.png')
    plt.close()
    FFT=np.fft.fft(X)
    MAG=np.abs(FFT)**2
    freq=np.fft.fftfreq(X.shape[-1])
    plt.plot(freq,np.log10(MAG/np.nansum(MAG)))
    plt.ylabel("Log(Fractional Energy Spectral Density)")
    plt.xlabel("Frequency(1/Months)")
    plt.tight_layout()
    plt.title("Log FFT of "+long_name)
    plt.savefig(location+name+'/'+name+'_fft.png')
    np.save(location+name+'/'+name+'fft_frequency_range.npy',freq)
    np.save(location+name+'/'+name+'fft_magnitudes.npy',MAG)
    plt.close()
    plt.plot(np.log10(1/freq),np.log10(MAG/np.nansum(MAG)))
    plt.ylabel("Log(Fractional Energy Spectral Density)")
    plt.xlabel("Log(Period(Months))")
    plt.axvline(x=2.07918,color='k',linestyle='dashed')
    plt.axvline(x=3.07918,color='k',linestyle='dashed')
    plt.title("Log FFT of "+long_name)
    plt.tight_layout()
    plt.savefig(location+name+'/'+name+'_fft_period.png')
    indices=np.argsort(MAG)[-20:][::-1]
    frequencies=freq[indices]
    np.save(location+name+'/'+name+'_freqs.npy',frequencies)

    plt.close()
    plt.acorr(X,maxlags=24)
    plt.xlim((-1,25))
    plt.ylabel('Autocorrelation')
    plt.xlabel('Lag/Months')
    plt.title("Autocorrelation of "+long_name)
    plt.tight_layout()
    plt.savefig(location+name+'/'+name+'_acorr.png')

def analysisND(X,units,location,name,time_axis=0,area_axis=(1,2)):
    #general stats
    stats=np.zeros(4)
    stats[0]=np.mean(X)
    stats[1]=np.std(X)
    stats[2]=np.max(X)
    stats[3]=np.min(X)
    print(location+name+'/stats.npy')
    np.save(location+name+'/stats.npy',stats)
    #General area averaged plots
    non_time_axis=np.delete(np.arange(0,len(np.shape(X))),time_axis)
    area_averaged=np.mean(X,axis=non_time_axis)
    plt.close()
    plt.plot(area_averaged)
    plt.ylabel(units)
    plt.xlabel('time(months)')
    plt.savefig(location+name+'/1D_plot.png')
    plt.close()
    FFT=np.fft.fft(area_averaged)
    MAG=np.abs(FFT)**2
    freq=np.fft.fftfreq(area_averaged.shape[-1])
    plt.plot(freq,MAG/np.nansum(MAG))
    plt.ylabel("Fractional Energy Spectral Density")
    plt.xlabel("Frequency(1/Months)")
    plt.savefig(location+name+'/fft.png')
    plt.close()
    plt.acorr(area_averaged,maxlags=24)
    plt.xlim((-1,25))
    plt.ylabel('Autocorrelation')
    plt.xlabel('Lag/Months')
    plt.savefig(location+name+'/acorr.png')
    #Non-area-averaged plots
    plt.hist(X,bins=100)
    plt.ylabel('Frequency')
    plt.xlabel(units)
    plt.savefig(location+name+'/hist.png')
    plt.close()
    non_area_axis=np.delete(np.arange(0,len(np.shape(X))),area_axis)
    amean=np.mean(X,axis=non_area_axis)
    plt.pcolor(amean)
    plt.colorbar()
    plt.savefig(location+name+'/amean.png')
    astd=np.std(X,axis=non_area_axis)
    plt.pcolor(astd)
    plt.colorbar()
    plt.savefig(location+name+'/astd.png')
    plt.close()
    #This assumes that the first axis is the time axis
    RX=np.reshape(X,(np.shape(X)[0],np.size(X)/np.shape(X)[0]))
    RX=np.nan_to_num(RX)
    pca=PCA(n_components=5)
    pca.fit(RX)
    EVR=np.reshape(pca.explained_variance_ratio_,(np.shape(X)[1:]))
    SV=np.reshape(pca.singular_values_,(np.shape(X)[1:]))
    np.save(location+name+'/pca_evr.npy',EVR)
    np.save(location+name+'/pca_sv.npy',SV)
    COMP=np.reshape(pca.components_,(5,np.shape(X)[1:]))
    np.save(location+name+'/pca_comp.npy',PCA)
    for i in range(0,5):
        plt.pcolor(COMP[i])
        plt.title('PCA Component {}'.format(i+1))
        plt.savefig(location+name+'/pca_comp{}.png'.format(i+1))
        plt.close()



