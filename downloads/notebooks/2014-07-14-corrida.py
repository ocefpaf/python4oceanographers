# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from IPython.core.display import HTML

with open('creative_commons.txt', 'r') as f:
    html = f.read()
    
with open('./styles/custom.css', 'r') as f:
    styles = f.read()
    
HTML(styles)

name = '2014-07-14-corrida'

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

# I added together two of my hobbies (running and python) into one python
# package ;):  [python-corrida](https://github.com/ocefpaf/python-corrida) is
# a small module based on a Fortran program originally designed by
# [Paulo Polito](http://www.io.usp.br/Paulo+S.+Polito).  The module computes a
# spreadsheet for your training.  It was based on a paper that,
# unfortunately, no one seems to find it anymore...
# Still, it [works](https://github.com/ocefpaf/python-corrida/blob/master/test/corrida_original.csv)!
# 
# In addition to the training spreadsheet the module can convert `GPX` data from
# hand-held or phone GPS to a GeoJSON that is rendered automagically by github.
# 
# For the `GPX` to `GeoJSON `conversion all you need is
# [GDAL](https://pypi.python.org/pypi/GDAL/).  If you want to use the
# command line interface the command is:
# 
# `ogr2ogr -f "GeoJSON" Running.json Running.gpx tracks`
# 
# If you want a the python interface, here is a small script I wrote to do the
# same as above.  It extract only 1 track and the geometry for that track.  Most
# `GPX` from phone apps are in that format, so no harm there.  By extracting just
# the geometry the `GeoJSON` will be ready to be rendered by
# [github](https://github.com/ocefpaf/python-corrida/blob/master/plotting/GeoJSON/2013-02-03-Running.geojson).
# And [here](https://github.com/ocefpaf/python-corrida/blob/master/plotting/gpx_to_json.py)
# the script that performs the conversion.
# 
# If you wish to plot it locally just
# use [mplleaflet](https://github.com/jwass/mplleaflet) like in the example below.

# <codecell>

import os
import json

import numpy as np
import matplotlib.pyplot as plt

import mplleaflet

with open('./data/2013-04-29-Running.geojson') as f:
    gj = json.load(f)
    
xy = np.array(gj['coordinates']).squeeze()

fig, ax = plt.subplots()
ax.plot(xy[:,0], xy[:,1], color='#FFA500', linewidth=2)

mplleaflet.display(fig=ax.figure)

# <codecell>

HTML(html)

