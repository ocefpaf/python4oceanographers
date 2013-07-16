title: Plotting AVISO track from their kmz file
date:  2013-07-14 15:15
category: Plotting
tags: AVISO, plotting, SSH
slug: plotting
author: Filipe Fernandes
summary: Simple function to load data inside the AVISO kmz file and plot the
satellite tracks.


AVISO [Altimetry](http://www.aviso.oceanobs.com/en/altimetry.html) data is
available in two formats gridded and along track data.  Sometime the track data
is desirable to augment hydrographic data due to its higher resolution and/or
to avoid the several assumptions done for the grid interpolation.  For that one
must find the neatest track to the area of interest.  The AVISO group provide a
nice kmz [compilation](http://www.aviso.oceanobs.com/en/data/tools/pass-locator.html) with all the satellites tracks and availability in time:


The [kmz](http://en.wikipedia.org/wiki/Keyhole_Markup_Language) is just a
compressed kml.  So it is straight forward to unzip it and read its information
with a simple python script.  First we will need to import zipfile and a kml
parser

{% notebook AVISO_tracks.ipynb cells[0:1] %}


Then we need to define a function to read the kmz file:

{% notebook AVISO_tracks.ipynb cells[1:2] %}

To find the nearest track I used a simple [knn_search](http://glowingpython.blogspot.com.br/2012/04/k-nearest-neighbor-search.html)
function. Here is the final result.

{% notebook AVISO_tracks.ipynb cells[5:6] %}
