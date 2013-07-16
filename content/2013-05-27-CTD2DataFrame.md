title: Pandas for CTD data
date:  2013-05-27 07:19
category: Data analysis
tags: CTD, pandas, data analysis, plotting
slug: CTD2DataFrame
author: Filipe Fernandes
summary: Reading SeaBird CNV format directly into a pandas DataFrame.

[Pandas](http://pandas.pydata.org/) is an amazing python module to deal with
data.  It has tons of features worthwhile learning, but the best of all is how
quick one can explore a data with just a few code lines once you learn the
basics.

I wrote a small [module](http://code.google.com/p/python-oceans/source/browse/oceans/ctd/ctd.py#619)
to read CTD (also XBT's EDF and FSI's CTD format) data directly as a pandas
DataFrame.  Here is an example how to use it:

{% notebook CTD2DataFrame.ipynb cells[1:2] %}

That's it the compressed [SeaBird](http://www.seabird.com/software/SBEDataProcforWindows.htm) cnv file is loaded
into memory.

If you have the Rossete file you can load and make a simple bottle summary with just two lines:

{% notebook CTD2DataFrame.ipynb cells[2:3] %}

Metadata and data flags are easily accessed.

{% notebook CTD2DataFrame.ipynb cells[3:4] %}

Cleaning the DataFrame and manipulating the variables inside it is straight
forward:

{% notebook CTD2DataFrame.ipynb cells[4:5] %}

There are some rudimentary CTD processing steps similar to those found in the
SBE Software:

{% notebook CTD2DataFrame.ipynb cells[6:11] %}

This also allows for a more customize "derived" step:

{% notebook CTD2DataFrame.ipynb cells[11:12] %}

Last but not least a handy way for plotting the data:

{% notebook CTD2DataFrame.ipynb cells[12:15] %}
