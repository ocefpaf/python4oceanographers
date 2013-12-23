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

{% notebook thermal_mass.ipynb cells[2:5] %}

The file **CTD-before.cnv.gz** is just the raw data acquired be the CTD.  The
file **CTD-after.cnv.gz** had both the `Align` (-0.01 s and 0.07 s for the
primary and secondary conductivity sensors respectively as provided by the
calibration lab) and the `Cell Thermal Mass` ($\alpha = 0.03$ for
thermal anomaly amplitude and  $\tau = 7$ s for the time constant) corrections
applied.

Here is the result of such "corrections":

{% notebook thermal_mass.ipynb cells[5:6] %}

Unfortunately most people apply those corrections using the defaults on the SBE
Software and then "correct" the bad corrections with averaging, smoothing, and
despiking techniques.  A much better solution is to estimate these parameters
for your CTD system and avoid them altogether.

[id]: http://dx.doi.org/10.1175/1520-0426(1990)007<0741:TIOCCT>2.0.CO;2 "Lueck, R.G., 1990: Thermal Inertia of Conductivity Cells: Theory., American Meteorological Society Oct 1990, 741-755."
