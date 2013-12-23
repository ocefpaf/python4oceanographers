Title: Removing spikes from CTD data &mdash; Part 1
date:  2013-06-03 04:03
comments: true
slug: ctd_spikes_1


There are two different types of spikes that may happen in CTD data:

1.  Bad data from electrical failures.  Usually it manifest in all the measured
    variables (Temperature, Conductivity, Oxygen, etc);
2.  Salinity spikes due to a wrong temperature value used when computing it
    from conductivity.  This can happen due to a a bad Alignment of the
    temperature and conductivity sensors and/or poor Cell thermal mass
    correction [(Lueck 1990)][id].

The second case is a little bit more complex and will be discussed in another
post.  However, when bad data appears one must create a set criteria to
eliminate them.  It varies from manually excluding them to several "objective"
criteria.

[SBE](http://www.seabird.com/software/sbedataprocforwindowsdetails.htm)
software calls it **Wild Edit** and performs a very similar technique to the
two-pass criteria from a previous post.

Here is a typical spike in the salinity data:

{% notebook ctd_spike.ipynb cells[5:] %}


The parameters used where:

{% notebook ctd_spike.ipynb cells[4:5] %}

The first pass just flag the data that is more than 2 standard deviations from
the mean and hide them from the second pass.  The second pass then flags the
remaining data points that are more than 20 standard deviations from the mean.

**2**, **20** , **500** are not magical numbers!  They are the same values
suggested in the SBE Software defaults, probably tested to exhaustion for CTD
data.

[id]: http://dx.doi.org/10.1175/1520-0426(1990)007<0741:TIOCCT>2.0.CO;2 "Lueck, R.G., 1990: Thermal Inertia of Conductivity Cells: Theory., American Meteorological Society Oct 1990, 741-755."
