# -*- coding: utf-8 -*-
#
# plt_profiles.py
#
# purpose:  Load and plot CTD profiles
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.tiddlyspot.com/
# created:  13-Nov-2012
# modified: Wed 14 Nov 2012 06:56:31 PM BRST
#
# obs:
#

import os
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as AA
from mpl_toolkits.axes_grid1 import host_subplot

font = {'size': 9}
plt.rc('font', **font)

deg = u"\u00b0"

#est = raw_input("Enter the CTD station to plot: [01 to 15]: ")
est = 15
fname = 'estacao%s.dat' % est
fname = os.path.join('..', 'data', fname)

P, T, S = np.loadtxt(fname, unpack=True, usecols=(0, 3, 4), skiprows=1)

fig = plt.figure(figsize=(4.2, 6))

ax0 = host_subplot(111, axes_class=AA.Axes)
new = ax0.get_grid_helper()
ax0.axis["bottom"] = new.new_fixed_axis(loc="bottom",
                                        offset=(0, -40),
                                        axes=ax0)
p0, = ax0.plot(T, P, linewidth=2.0, color='green', label=r'Temperature')

ax0.set_ylabel("Pressure [dbar]")
ax0.set_xlabel(u"Temperature[%sC]" % deg)
ax0.axis["bottom"].label.set_color(p0.get_color())
ax0.set_title("CTD %s" % est)

ax1 = ax0.twiny()
new = ax1.get_grid_helper()
ax1.axis["top"] = new.new_fixed_axis(loc="bottom",
                                     offset=(0, 0),
                                     axes=ax1)
p1, = ax1.plot(S, P, linewidth=2.0, color='blue', label=r'Salinity')

ax1.set_xlabel("Salinity [Kg g$^{-1}$]")
ax1.axis["top"].label.set_color(p1.get_color())
ax1.invert_yaxis()
ax1.axis("tight")

ax0.legend(shadow=True, fancybox=True, numpoints=1,
           loc=2, bbox_to_anchor=(.6, 0.2))

fig.savefig("CTD_profile_%s.svg" % est, transparent=True)

plt.show()
