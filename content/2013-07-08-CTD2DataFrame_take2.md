Title: CTD2DataFrame take 2
date:  2013-07-08 07:19
comments: true
slug: CTD2DataFrame_2


The easiest way to obtain the **ctd.py** module used in previous posts is to
[download](http://code.google.com/p/python-oceans/) the source code for
the **oceans** python module and add the python-oceans/oceans directory to your
`PYTHONPATH` similar to what we done for the python-gsw.

To clone the repository using mercurial type:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.bash}
hg clone https://code.google.com/p/python-oceans/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
and to update:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.bash}
hg pull
hg update
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now you can import the pandas modified **DataFrame** and load CTD (SeaBird
`CNV` and FSI `ASCII` formats) and XBT (`EDF`) files directly.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ {.python}
from oceans.ctd import DataFrame
seabird_cast = DataFrame.from_cnv(fname)
fsi_cast = DataFrame.from_fsi(fname)
xbt = DataFrame.from_edf(fname)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The available methods are:

*   `split`: Separate upcast from downcast.
*   `plot_vars`: Plot two variables together (usually Salinity and Temperature).
*   `swap_index`: Change the index (usually from pressure to depth or scan count).
*   `press_check`: Check for pressure inversions.
*   `get_maxdepth`: Cast maximum depth.
*   `plot_section`:  If the DataFrame is a collection of CTD stations this plot
    the section.

There is also a modified pandas **Series** (1D DataFrames) with the following
methods:

*   `plot`: Plot the CTD profile.
*   `smooth`: Smooth the profile.
*   `despike`: Remove spikes from the data.
*   `bindata`: Performs a bin average.
