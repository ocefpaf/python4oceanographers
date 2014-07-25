# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import iris
import iris.plot as iplt
import matplotlib.pyplot as plt
%matplotlib inline

# Add the .html in the end to visualize in the browser.
url = 'http://data.nodc.noaa.gov/thredds/dodsC/testdata/netCDFTemplateExamples/profile/wodStandardLevels.nc'
sal = iris.load_cube(url, 'sea_water_salinity')

print(sal)

# <codecell>

lon = iris.Constraint(longitude=lambda l:100 < l < 150)
lat = iris.Constraint(latitude=lambda l:-40 < l < -20)
alt = iris.Constraint(altitude=lambda a: a <= 30)
sal_profile = sal.extract(alt & lon & lat)
print(sal_profile)

# <codecell>

fig, ax = plt.subplots()

x = sal.coord('longitude').points
y = sal.coord('latitude').points

xc = sal_profile.coord('longitude').points
yc = sal_profile.coord('latitude').points

ax.plot(x, y, 'ko')
ax.plot(xc, yc, 'ro')
ax.grid()

# <codecell>

fig, ax = plt.subplots(figsize=(5, 6))
iplt.plot(sal_profile, sal_profile.coord('altitude'),
          linewidth=2,  color='k')
ax.set_xlabel('Salinity')
ax.set_ylabel('Depth')

