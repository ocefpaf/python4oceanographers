Title: Plotting AVISO track using a kmz file
date:  2013-06-24 15:15
comments: true
slug: plotting


AVISO [Altimetry](http://www.aviso.oceanobs.com/en/altimetry.html) data is
available in two formats, gridded and along-track data.  Sometimes the
along-track data is desirable, instead of the gridded data, to augment
hydrographic data.  The along-track has a higher spatial and avoids the several
assumptions made for the grid interpolation.

This example helps to find the nearest track to a point of interest.  The AVISO
group provide a nice kmz [compilation](http://www.aviso.oceanobs.com/en/data/tools/pass-locator.html) with all the satellites tracks and availability in time:

The [kmz](http://en.wikipedia.org/wiki/Keyhole_Markup_Language) format is just
a compressed kml.  So it is straight forward to unzip it and read its information
with a simple python script.  First we will need to `import zipfile` and a
`KML` parser,

{% notebook AVISO_tracks.ipynb cells[1:2] %}

Then we need to define a function to read the kmz file:

{% notebook AVISO_tracks.ipynb cells[2:3] %}

To find the nearest track we used a simple [knn_search](http://glowingpython.blogspot.com.br/2012/04/k-nearest-neighbor-search.html)
function. Here is the final result.

{% notebook AVISO_tracks.ipynb cells[6:7] %}
