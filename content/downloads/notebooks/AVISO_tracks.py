# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import zipfile
import numpy as np
import matplotlib.pyplot as plt

from fastkml.kml import KML
from mpl_toolkits.basemap import Basemap

# <codecell>

def read_kmz(fname):
    r"""Reads AVISO kmz file and return a dictionary with tracks as
    keys and position (lon, lat) as values."""
    zfile = zipfile.ZipFile(fname)
    kml_string = zfile.read(zfile.filelist[0].filename)

    kml = KML()
    kml.from_string(kml_string)
    Document, Folder, SubFolder, PlaceMark = [], [], [], []
    tracks, points = dict(), dict()
    for Document_feat in kml.features():  # 1 level.
        Document.append(Document_feat)
        for Folder_feat in Document_feat.features():  # 2 levels line and dots.
            Folder.append(Folder_feat)
            for SubFolder_feat in Folder_feat.features():  # 20 levels
                SubFolder.append(SubFolder_feat)
                for PlaceMark_feat in SubFolder_feat.features():
                    if PlaceMark_feat.styleUrl == '#LINE':  # 254 level tracks.
                        PlaceMark.append(PlaceMark_feat)
                        track = PlaceMark_feat.name
                        pos = PlaceMark_feat.geometry.xy
                        tracks.update({track: pos})
                    if PlaceMark_feat.styleUrl == '#DOT':
                        track = PlaceMark_feat.name
                        pos = PlaceMark_feat.geometry.wkt
                        points.update({track: pos})
    return tracks

# <codecell>

def plt_tracks(tracks, color, **kw):
    for track, (lon, lat) in tracks.iteritems():
        lon, lat = map(np.array, (lon, lat))
        # Prevent matplotlib from connecting the lines.
        mask = lon >=0
        m.plot(*m(lon[mask], lat[mask]), color=color, **kw)
        m.plot(*m(lon[~mask], lat[~mask]), color=color, **kw)

# <codecell>

def make_map(lonStart=-50, lonEnd=-40, latStart=-30, latEnd=-21,
             image=None):
    fig, ax = plt.subplots(figsize=(8, 8))
    # Setted for nautical chart 01.
    m = Basemap(projection='merc', llcrnrlon=-59, urcrnrlon=-25,
                llcrnrlat=-38, urcrnrlat=9, lat_ts=-26, resolution='i')
    m.ax = ax

    if image:
        img = plt.imread(image)
        m.imshow(img, origin='upper', alpha=0.45)
    else:
        m.drawcoastlines()
        m.fillcontinents()

    lon_lim, lat_lim = m([lonStart, lonEnd], [latStart, latEnd])
    m.ax.axis([lon_lim[0], lon_lim[1], lat_lim[0], lat_lim[1]])

    meridians = np.arange(lonStart, lonEnd, 1.5)
    parallels = np.arange(latStart,  latEnd, 1.5)
    xoffset = -lon_lim[0] + 1e4
    yoffset = -lat_lim[0] + 1e4
    kw = dict(linewidth=0)
    m.drawparallels(parallels, xoffset=xoffset, labels=[1, 0, 0, 0], **kw)
    m.drawmeridians(meridians, yoffset=yoffset, labels=[0, 0, 0, 1], **kw)
    return fig, m

# <codecell>

def knn_search(x, D, n):
    ndata = D.shape[1]
    n = n if n < ndata else ndata
    sqd = np.sqrt(((D - x[:, :ndata]) ** 2).sum(axis=0))
    return sqd

def find_nearst_track(tracks, point=(-44, -28.5)):
    name, dist = None, 1e4
    point = np.atleast_2d(point).T
    for track, data in tracks.items():
        data = np.atleast_2d(data)
        new_dist = knn_search(point, data, 1).min()
        if new_dist < dist:
            name = track
            dist = new_dist
    print("Nearest track: %s" % name)
    return tracks[name]

# <codecell>

tracks = read_kmz('./data/Visu_J1TP_Interlaced_Tracks_GE_V3.kmz')

fig, m = make_map()
lon, lat = -44, -28.5  # Some Buoy.
kw = dict(marker='o', linestyle='none', markersize=8, markeredgecolor='w',
          zorder=2)

m.plot(*m(lon, lat), label='Buoy', markerfacecolor='#2e64fe', **kw)

# Altimeter tracks.
kw = dict(alpha=0.7, linewidth=3, solid_capstyle='round', zorder=1)
plt_tracks(tracks, color='#848484', **kw)

# Closest track to the buoy.
lon, lat = find_nearst_track(tracks, point=(lon, lat))
m.plot(*m(lon, lat), label=u'Nearest altimeter track', color='#f2123f', **kw)
_ = m.ax.legend(numpoints=1, loc=2)

