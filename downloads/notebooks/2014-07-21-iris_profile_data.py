# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from IPython.core.display import HTML

with open('creative_commons.txt', 'r') as f:
    html = f.read()
    
with open('./styles/custom.css', 'r') as f:
    styles = f.read()
    
HTML(styles)

name = '2014-07-21-iris_profile_data'

html = """
<small>
<p> This post was written as an IPython notebook.  It is available for
<a href="http://ocefpaf.github.com/python4oceanographers/downloads/
notebooks/%s.ipynb">download</a> or as a static
<a href="http://nbviewer.ipython.org/url/ocefpaf.github.com/
python4oceanographers/downloads/notebooks/%s.ipynb">html</a>.</p>
<p></p>
%s """ % (name, name, html)

%matplotlib inline

# <markdowncell>

# I am looking into the CF-standards for
# [profile data](http://cfconventions.org/Data/cf-convetions/cf-conventions-1.7/build/cf-conventions.html#idm43165503776) to implement a
# netCDF save option for [python-ctd](https://github.com/ocefpaf/python-ctd).
# 
# Until now I was using a customized HDF5 file that, even though it was practical,
# the file was useless for software like iris.  Iris obeys the CF-standards rules and rejects
# data that does not comply to it.  Here is an iris example for
# [plotting](http://scitools.org.uk/iris/docs/latest/examples/graphics/atlantic_profiles.html)
# profile data.
# 
# I decided to try it with a netCDF that was created with the CF profile standards to see how easy
# it would be to load and plot it once I implement the rules in `python-ctd`.
# 
# Here is the result:

# <markdowncell>

# First lets load `sea_water_sality` cube from a profile example file provided by
# [NODC](http://data.nodc.noaa.gov/thredds/dodsC/testdata/netCDFTemplateExamples/profile/wodStandardLevels.nc.html).

# <codecell>

import iris

url = 'http://data.nodc.noaa.gov/thredds/dodsC/testdata/netCDFTemplateExamples/profile/wodStandardLevels.nc'
sal = iris.load_cube(url, 'sea_water_salinity')

print(sal)

# <markdowncell>

# The dimension coordinate has 169 profiles by 26 altitude (positive down, AKA depth!),
# and the auxiliary coordinates are in the 169 Dimension coordinate.
# That means I have 169 profiles and the positions are stored in the auxiliary coordinates.
# Very different from model data were the Dimension coordinate are usually the positions.
# 
# Before we try to extract a profile lets plot the data positions
# to understand what the profile rules are all about. 

# <codecell>

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from cartopy.feature import LAND, COASTLINE
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

x = sal.coord('longitude').points
y = sal.coord('latitude').points

fig, ax = plt.subplots(figsize=(11, 13),
                       subplot_kw=dict(projection=ccrs.PlateCarree()))
ax.set_extent([-180, 180, -90, 90])
ax.stock_img()
ax.plot(x, y, 'go')

ax.add_feature(COASTLINE)
kw = dict(linewidth=1.5, color='gray', alpha=0.5, linestyle='--')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, **kw)
gl.xlabels_top = gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

from shapely.geometry.polygon import LinearRing
lons = [105, 105, 125, 125]
lats = [-40, -20, -20, -40]
ring = LinearRing(list(zip(lons, lats)))
sq = ax.add_geometries([ring], ccrs.PlateCarree(), facecolor='none', edgecolor='red')

# <markdowncell>

# OK, so we want that one profile inside the square!  Lets build the iris
# `Constraint` for that box.  We will also limit the depth of the of the data to 30 m
# avoid loading missing data from below it.  (That is a shallow profile, but it serve our
# purpose.)

# <codecell>

lon = iris.Constraint(longitude=lambda l:min(lons) < l < max(lons))
lat = iris.Constraint(latitude=lambda l:min(lats) < l < max(lats))
alt = iris.Constraint(altitude=lambda a: a <= 30)

sal_profile = sal.extract(alt & lon & lat)

print(sal_profile)

# <markdowncell>

# And finally the profile plot:

# <codecell>

import iris.plot as iplt

lon = sal_profile.coord(axis='X').points.squeeze()
lat = sal_profile.coord(axis='Y').points.squeeze()
depth = sal_profile.coord(axis='Z').points.max()

fig, ax = plt.subplots(figsize=(5, 6))
kw = dict(linewidth=2,  color='k', marker='o')
iplt.plot(sal_profile, sal_profile.coord('altitude'), **kw)
ax.grid()
ax.set_ylabel('Depth (m)')
ax.set_xlabel('Salinity (unknown)')
t = ax.set_title('lon: %s\nlat: %s\nMax depth = %s' % (lon, lat, depth))

# <markdowncell>

# Soon `python-ctd` will be saving files according the CF profile
# standards, and we will be using iris to expore the data.

# <codecell>

HTML(html)

