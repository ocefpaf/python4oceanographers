# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

fig, ax = plt.subplots(subplot_kw=dict(projection=ccrs.PlateCarree()))

url = 'http://map1c.vis.earthdata.nasa.gov/wmts-geo/wmts.cgi'
layer_name = 'VIIRS_CityLights_2012'
ax.set_extent([-15, 25, 35, 60])
ax.add_wmts(url, layer_name)

