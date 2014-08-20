# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from IPython.core.display import HTML

with open('creative_commons.txt', 'r') as f:
    html = f.read()
    
with open('./styles/custom.css', 'r') as f:
    styles = f.read()
    
HTML(styles)

name = '2014-08-11-gpx'

html = """
<small>
<p> This post was written as an IPython notebook.  It is available for
<a href="http://ocefpaf.github.com/python4oceanographers/downloads/
notebooks/%s.ipynb">download</a> or as a static
<a href="http://nbviewer.ipython.org/url/ocefpaf.github.com/
python4oceanographers/downloads/notebooks/%s.ipynb">html</a>.</p>
<p></p>
%s """ % (name, name, html)

import seaborn
%matplotlib inline

# <markdowncell>

# This post is an exercise on how to explore GPX files.  Most of what I did in
# this post learned from this
# [tutorial](http://nbviewer.ipython.org/github/titsworth/hsvpy-runtalk/tree/master/).
# 
# Deep down the GPX file format is just a XML document text.  They can be parsed
# with any XML parser out there, but the
# [gpxpy](http://www.trackprofiler.com/gpxpy/index.html) module makes that task
# much easier.  Here is a quick example on how to load and explore the data
# inside a GPX file.

# <codecell>

import gpxpy
gpx = gpxpy.parse(open('./data/2014_08_05_farol.gpx'))

print("{} track(s)".format(len(gpx.tracks)))
track = gpx.tracks[0]

print("{} segment(s)".format(len(track.segments)))
segment = track.segments[0]

print("{} point(s)".format(len(segment.points)))

# <markdowncell>

# Now lets extract the data for all those points.  Here I have 1 track and 1
# segment, but a GPX file might contain multiple tracks and segments.  The
# best practice here is to always loop through all tracks and segments.

# <codecell>

data = []
segment_length = segment.length_3d()
for point_idx, point in enumerate(segment.points):
    data.append([point.longitude, point.latitude,
                 point.elevation, point.time, segment.get_speed(point_idx)])
    
from pandas import DataFrame

columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
df = DataFrame(data, columns=columns)
df.head()

# <markdowncell>

# I want to plot the direction of the movement with a quiver plot.  For that I
# will need the `u` and `v` velocity components.  And to compute `u` and `v` I
# need the angle associated to each speed data.  Instead of re-inventing the
# wheel I will use the `seawater` library `sw.dist` function to calculate the
# angles.
# 
# I also smoothed the data a little bit to improve the plot.
# (GPX data from smart-phones can be very noisy.)

# <codecell>

import numpy as np
import seawater as sw
from oceans.ff_tools import smoo1

_, angles = sw.dist(df['Latitude'], df['Longitude'])
angles = np.r_[0, np.deg2rad(angles)]

# Normalize the speed to use as the length of the arrows
r = df['Speed'] / df['Speed'].max()
kw = dict(window_len=31, window='hanning')
df['u'] = smoo1(r * np.cos(angles), **kw)
df['v'] = smoo1(r * np.sin(angles), **kw)

# <markdowncell>

# Now lets use [mplleaflet](https://github.com/jwass/mplleaflet) to plot the
# track and the direction.

# <codecell>

import mplleaflet
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
df = df.dropna()
ax.plot(df['Longitude'], df['Latitude'],
        color='#0101DF', linewidth=5, alpha=0.5)
sub = 10
ax.quiver(df['Longitude'][::sub], df['Latitude'][::sub], df['u'][::sub], df['v'][::sub], color='#B40404', alpha=0.5, scale=10)
mplleaflet.display(fig=ax.figure)

# <markdowncell>

# If you have tons of GPX files with your run data, it might come in handy to define a function to read them all at once.

# <codecell>

import os
from glob import glob

def load_run_data(gpx_path, filter=""):
    gpx_files = glob(os.path.join(gpx_path, filter + "*.gpx"))
    run_data = []
    for file_idx, gpx_file in enumerate(gpx_files): 
        gpx = gpxpy.parse(open(gpx_file, 'r'))
        # Loop through tracks
        for track_idx, track in enumerate(gpx.tracks):
            track_name = track.name
            track_time = track.get_time_bounds().start_time
            track_length = track.length_3d()
            track_duration = track.get_duration()
            track_speed = track.get_moving_data().max_speed
            
            for seg_idx, segment in enumerate(track.segments):
                segment_length = segment.length_3d()
                for point_idx, point in enumerate(segment.points):
                    run_data.append([file_idx, os.path.basename(gpx_file), track_idx, track_name, 
                                     track_time, track_length, track_duration, track_speed, 
                                     seg_idx, segment_length, point.time, point.latitude, 
                                     point.longitude, point.elevation, segment.get_speed(point_idx)])
    return run_data

# <codecell>

data = load_run_data(gpx_path='./data/GPX/', filter="")
df = DataFrame(data, columns=['File_Index', 'File_Name', 'Index', 'Name',
                              'Time', 'Length', 'Duration', 'Max_Speed',
                              'Segment_Index', 'Segment_Length', 'Point_Time', 'Point_Latitude',
                              'Point_Longitude', 'Point_Elevation', 'Point_Speed'])

HTML(df.head().to_html(max_cols=4))

# <markdowncell>

# Here I will clean up the DataFrame and convert the distances to km.

# <codecell>

cols = ['File_Index', 'Time', 'Length', 'Duration', 'Max_Speed']
tracks = df[cols].copy()
tracks['Length'] /= 1e3
tracks.drop_duplicates(inplace=True)
tracks.head()

# <markdowncell>

# And finally lets add  a Track Year and Month columns based on track time.
# That way we can explore the run data with some stats and bar plots.

# <codecell>

tracks['Year'] = tracks['Time'].apply(lambda x: x.year)
tracks['Month'] = tracks['Time'].apply(lambda x: x.month)
tracks_grouped = tracks.groupby(['Year','Month'])
tracks_grouped.describe().head()

# <codecell>

figsize=(7, 3.5)

tracks_grouped = tracks.groupby(['Year', 'Month'])
ax = tracks_grouped['Length'].sum().plot(kind='bar', figsize=figsize)
xlabels = [text.get_text() for text in  ax.get_xticklabels()]
ax.set_xticklabels(xlabels, rotation=70)
_ = ax.set_ylabel('Distance (km)')

# <markdowncell>

# Bad news!  My goal was to run 50 km per month... I am clear way too far from
# accomplishing it!  (Not to mentioned the fact that there is no data from 2014!)

# <markdowncell>

# To close this post I want to produce a plot similar to
# [this](http://flowingdata.com/2014/02/05/where-people-run/)
# using my run data.

# <codecell>

def load_run_data(gpx_path, filter=""):
    gpx_files = glob(os.path.join(gpx_path, filter+"*.gpx"))    
    run_data = []
    for file_idx, gpx_file in enumerate(gpx_files): 
        try:
            gpx = gpxpy.parse(open(gpx_file, 'r'))
        except: 
            os.remove(gpx_file)
            continue
        run_data_tmp = [[file_idx, gpx_file, point.latitude,point.longitude, point.elevation] 
                            for track in gpx.tracks 
                                for segment in track.segments 
                                    for point in segment.points]
        run_data += run_data_tmp
    return run_data

def clear_frame(ax): 
    ax.xaxis.set_visible(False) 
    ax.yaxis.set_visible(False) 
    for spine in ax.spines.values(): 
        spine.set_visible(False)
        
def plot_run_data(coords, **kwargs):
    columns = ['Index', 'File_Name', 'Latitude', 'Longitude', 'Altitude']
    coords_df = DataFrame(coords, columns=columns)
    grouped = coords_df.groupby('Index')
    
    fig, ax = plt.subplots(figsize=kwargs.get('figsize', (13 ,8)))

    bgcolor = kwargs.get('bgcolor', '#001933')
    color = kwargs.get('color', '#FFFFFF')
    linewidth = kwargs.get('linewidth', .035)
    alpha = kwargs.get('alpha', 0.5)

    kw = dict(color=color, linewidth=linewidth, alpha=alpha)
    grouped.plot('Longitude', 'Latitude', **kw)
    ax.grid(False)
    ax.patch.set_facecolor(bgcolor)
    ax.set_aspect('auto','box','C')
    clear_frame(ax)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=.1)
    return ax

# <codecell>

df = load_run_data(gpx_path='./data/GPX/')
ax = plot_run_data(df, figsize=(4, 3), alpha=0.85,
                   bgcolor='#0A2A0A')
_ = ax.axis([-46.74, -46.71, -23.57, -23.55])

# <markdowncell>

# I tried to find public run data for Salvador to discover the best places to run
# here using that kind of plot.  First I tried [RunKeeper](http://runkeeper.com/),
# the app does make their public data available online, but it is not a popular
# app in Brazil and I could not find any tracks for Salvador in the database.
# [Sportstraker](http://www.sports-tracker.com/), on the other hand, is very
# popular here.  But Sportstraker do not publish the public data online.
# 
# If you read this and have some GPX files data from your training and want to
# see a map of Salvador most popular places to run, get in touch!

# <codecell>

HTML(html)

