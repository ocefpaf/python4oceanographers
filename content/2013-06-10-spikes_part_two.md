Title: Removing spikes from CTD data &mdash; Part 2
date:  2013-06-10 04:03
comments: true
slug: ctd_spikes_2

There are two different types of spikes that may happen in CTD data:

1.  Bad data from electrical failures.  Usually it manifest in all the
    measured variables (Temperature, Conductivity, Oxygen, etc);
2.  Salinity spikes due to a wrong temperature value used when computing it
    from conductivity.  This can happen due to a a bad Alignment of the
    temperature and conductivity sensors, and/or poor Cell thermal mass
    correction [(Lueck 1990)][id].

How to detect the second case?  For a start they do not manifest in the raw
data.  This kind of spike is a product of bad pre-processing parameters (either
Align and/or Cell Thermal Mass).  For more information on this check the SBE
Software documentation and the Go-SHIP
[manual](http://www.go-ship.org/Manual/McTaggart_et_al_CTD.pdf)

[id]: http://dx.doi.org/10.1175/1520-0426(1990)007<0741:TIOCCT>2.0.CO;2 "Lueck, R.G., 1990: Thermal Inertia of Conductivity Cells: Theory., American Meteorological Society Oct 1990, 741-755."


{% notebook 2013-06-10-spikes_part_two.ipynb cells[1:] %}
