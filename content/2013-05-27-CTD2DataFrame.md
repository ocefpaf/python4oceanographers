Title: Pandas for CTD data
date:  2013-05-27 07:19
comments: true
slug: CTD2DataFrame

[Pandas](http://pandas.pydata.org/) is an amazing python module to deal with
data.  It has tons of features worthwhile learning, but the best of all is how
quick one can explore a data with just a few code lines once you learn the
basics.

I wrote a small [module](http://code.google.com/p/python-oceans/source/browse/oceans/ctd/ctd.py#619)
to read CTD (also XBT's EDF and FSI's CTD format) data directly as a pandas
DataFrame.  Here is an example how to use it:

{% notebook CTD2DataFrame.ipynb cells[2:3] %}

That's it! One line to load the compressed [SeaBird](http://www.seabird.com/software/SBEDataProcforWindows.htm) cnv file into
memory.  If you have the Rossete file you can load it as well and print the
bottle summary with just two lines:

{% notebook CTD2DataFrame.ipynb cells[3:4] %}

Metadata and data flags are also easily accessed.

{% notebook CTD2DataFrame.ipynb cells[4:5] %}

Cleaning the DataFrame and manipulating the variables:

{% notebook CTD2DataFrame.ipynb cells[5:6] %}

The module also contains some rudimentary CTD processing steps akin to those
found in the [SBE Software](ftp://ftp.halcyon.com/pub/seabird/OUT/SeasoftV2/SBEDataProcessing/):

{% notebook CTD2DataFrame.ipynb cells[7:12] %}

The module also allows for a more "customized" derive step:

{% notebook CTD2DataFrame.ipynb cells[12:13] %}

Last but not least, a handy way for plotting the data:

{% notebook CTD2DataFrame.ipynb cells[13:16] %}
