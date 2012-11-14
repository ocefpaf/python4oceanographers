# -*- coding: utf-8 -*-
#
# plt_TS.py
#
# purpose:  Plot a TS diagram
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.tiddlyspot.com/
# created:  13-Nov-2012
# modified: Wed 14 Nov 2012 06:55:16 PM BRST
#
# obs:
#

import os
from glob import glob

import numpy as np
import seawater.csiro as sw
import matplotlib.pyplot as plt

from pandas import DataFrame


def basename(fname):
    return os.path.splitext(os.path.basename(fname))


def read_station(fname):
    P, T, S = np.loadtxt(fname, unpack=True, usecols=(0, 3, 4), skiprows=1)
    column = basename(fname)[0]
    return (DataFrame(T, index=P, columns=[column]),
            DataFrame(S, index=P, columns=[column]))

lista = glob(os.path.join('..', 'data', '*.dat'))
lista.sort()

first = lista.pop(0)
tmp, sal = read_station(first)

for fname in lista:
    T, S = read_station(fname)
    tmp = tmp.join(T, how='right')
    sal = sal.join(S, how='right')

Te = np.arange(0, 32, 2)
Se = np.arange(32, 38.25, 0.25)

Sg, Tg = np.meshgrid(Se, Te)
cnt = np.arange(20, 34)

sigma_theta = sw.pden(Sg, Tg, 0, 0) - 1000

deg = u"\u00b0"

fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(sal, tmp, 'k.')
ax.set_ylabel("Temperatura %sC" % deg)
ax.set_xlabel("Salinidade [g kg$^{-1}$]")

cs = ax.contour(Se, Te, sigma_theta, colors='black', levels=cnt)
ax.clabel(cs, fontsize=9, inline=1, fmt='%2.1f')
ax.axis([31.8, 37.2, 0.0, 30.0])

fig.savefig("TS_diagram.svg", transparent=True)

plt.show()
