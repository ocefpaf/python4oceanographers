import os
from glob import glob
import numpy as np
import seawater.csiro as sw
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap, shiftgrid, cm

url = 'http://ferret.pmel.noaa.gov/thredds/dodsC/data/PMEL/etopo5.nc'
etopodata = Dataset(url)
print(etopodata.variables.keys())

topoin = etopodata.variables['ROSE'][:]
lons = etopodata.variables['ETOPO05_X'][:]
lats = etopodata.variables['ETOPO05_Y'][:]

plt.pcolormesh(lons, lats, topoin)
plt.axis("tight")
plt.savefig("topografia.png", dpi=60)