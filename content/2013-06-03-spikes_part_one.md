title: Removing spikes from CTD data -- Part 1
date:  2013-06-03 04:03
category: Data analysis
tags: CTD, hydrography, data analysis
slug: ctd_spikes_1
author: Filipe Fernandes
summary: Spikes in CTD data.

CTD data main contain, in general, two different types of spikes:
* Bad data from electrical failures.  Usually it manifest in all the measured
  variables (Temperature, Conductivity, Oxygen, etc);
* Salinity spikes due to a wrong temperature value when computing it from
  conductivity.  This effect may be due to a a bad Alignment of the temperature
  and conductivity sensors or poor Cell thermal mass correction.
  For more information check Lueck, R.G., 1990: Thermal Inertia of Conductivity
  Cells: Theory., American Meteorological Society Oct 1990, 741-755.
