Title: CTD-processing
date:  2013-07-29 03:43
comments: true
slug: python-ctd


I'm re-factoring the [python-oceans](http://code.google.com/p/python-oceans/source/checkout/)
module.  The first step was to create another module just for the CTD tools
([python-ctd](https://github.com/ocefpaf/python-ctd))

The new module is already at `PyPI` and the API will remain the same as before.
To install it type:

~~~~~~~~~~~~~~~ {.bash}
pip install ctd
~~~~~~~~~~~~~~~

Now we can import the module:
{% notebook ctd_proc_example.ipynb cells[2:3] %}

Let's define a function to streamline the CTD data processing.
{% notebook ctd_proc_example.ipynb cells[4:5] %}

And finally we can process all the files in a single loop.
{% notebook ctd_proc_example.ipynb cells[7:8] %}

The warning is due to an issue with the data files, where some numbers were
"glued" and the parser ended-up loading then as `objects` instead of `floats`.
That is not a big deal, usually those values are already flagged as bad data
during the Data Conversion step and will be removed once we apply the flag.

Note that, using the pandas `Panel.fromDict` and `OrderedDict`, we created
a `hydrographic section` where the stations are the `items`, the `minor` axis
represent the data, and the `major` axis is our index (pressure or depth).

To plot a temperature section we needed is to create a `cross section` in our
`Panel`.  Unfortunately, pandas loses the object meta-data when performing
slicing operations.  That is why we need to re-attach the longitude and
latitude information before plotting.

{% notebook ctd_proc_example.ipynb cells[9:10] %}

`CT` can be thought as a 2-D matrix with the pressure information as its index.
To create a single cast plot just plot one column using either the station name
or python indexing syntax:

{% notebook ctd_proc_example.ipynb cells[10:11] %}
