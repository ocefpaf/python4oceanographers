# -*- coding: utf-8 -*-
#
# plt_map.py
#
# purpose:  Read all stations and plot a map
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.tiddlyspot.com/
# created:  13-Nov-2012
# modified: Wed 14 Nov 2012 06:55:23 PM BRST
#
# obs: Plot a map and a depth profile for the CTD transect.
#

import os
from glob import glob

import numpy as np
import seawater.csiro as sw
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap, shiftgrid, cm

def break_lines(line):
    return [float(num) for num in line.strip().split()]


def get_topo(url, m):
    etopodata = Dataset(url)
    topoin = etopodata.variables['ROSE'][:]
    lons = etopodata.variables['ETOPO05_X'][:]
    lats = etopodata.variables['ETOPO05_Y'][:]
    topoin, lons = shiftgrid(180., topoin, lons, start=False)
    nx = int((m.xmax - m.xmin) / 5000.) + 1
    ny = int((m.ymax - m.ymin) / 5000.) + 1
    return m.transform_scalar(topoin, lons, lats, nx, ny)


# Shelf angle.
def bathymetry_angle(start=0, end=9):
    opposite = depth[end] - depth[start]
    adjacent = dist[end] - dist[start]
    return np.arctan2(-opposite, adjacent) * 180 / np.pi


lista = glob(os.path.join('..', 'data', '*.dat'))
lista.sort()

depth, lat, lon = [], [], []
for fname in lista:
    with open(fname, 'r') as f:
        lines = f.readlines()
        d, la, lo = break_lines(lines[0])[3:]
        lon.append(lo)
        lat.append(la)
        depth.append(d)


# Map.
offset = 2.5
llcrnrlon, urcrnrlon = min(lon) - offset, max(lon) + offset
llcrnrlat, urcrnrlat = min(lat) - offset, max(lat) + offset

m = Basemap(projection='merc',
            llcrnrlon=llcrnrlon,
            urcrnrlon=urcrnrlon,
            llcrnrlat=llcrnrlat,
            urcrnrlat=urcrnrlat,
            lat_ts=20, resolution='h')
fig, ax = plt.subplots(figsize=(7, 7))
m.ax = ax

url = 'http://ferret.pmel.noaa.gov/thredds/dodsC/data/PMEL/etopo5.nc'
topodat = get_topo(url, m)

im = m.imshow(topodat, cm.GMT_haxby)
m.drawstates()
m.drawcountries()
m.drawcoastlines()
m.plot(lon, lat, 'r*', latlon=True)
cb = m.colorbar(im, 'right', size='5%', pad='2%')
meridians = np.arange(int(llcrnrlon), int(urcrnrlon), 2.)
parallels = np.arange(int(llcrnrlat), int(urcrnrlat), 1.)
kw = dict(fontsize=20, fontweight='demibold')
m.drawparallels(parallels, labels=[1, 0, 0, 1], **kw)
m.drawmeridians(meridians, labels=[1, 1, 0, 1], **kw)

fig.savefig("../slides/station_map.svg", transparent=True)

# Profile.
dist, phaseangle = sw.dist(lon, lat, units='km')
dist = np.r_[0, np.cumsum(dist)] * 1e3
shelf = bathymetry_angle(0, 9)
slope = bathymetry_angle(9, 11)

fig, ax = plt.subplots(figsize=(7, 4), facecolor='w')
ax.fill_between(dist, max(depth), depth, color='0.75')
ax.plot(dist, depth, color='k')
ax.set_ylim(0, max(depth))
ax.set_xlim(-5, max(dist) + 10)
ax.invert_yaxis()
ax.set_ylabel("Depth [db]")
ax.set_xlabel("Distance [m]")
ax.plot(dist, len(dist) * [0], 'kv')
ax.text(50000, 500, 'Shelf angle:\n%2.2f degrees' % shelf)
ax.text(200000, 500, 'Slope angle:\n%2.2f degrees' % slope)
ax.xaxis.tick_bottom()

fig.savefig("../slides/profile.svg", transparent=True)

plt.show()
