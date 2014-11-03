# -*- coding: utf-8 -*-
#
# optinter.py
#
# purpose:
# author:   Filipe P. A. Fernandes
# e-mail:   ocefpaf@gmail
# web:      http://ocefpaf.github.io/
# created:  03-Nov-2014
# modified: Mon Nov  3 16:34:42 2014
#
# obs:
#

def ff_function(a, x, fx, method='Markov'):
    """Compute the mean squared misfit between an analytical function
    (e.g. Gaussian or Markov function) and a set of data FX observed at
    independent coordinates X.

    Parameters
    ----------
    a : float
        Parameters of analytically function
    x : array
        Locations of data
    fx : array
         Observed function values (data).

    method : string
            Specifies the shape of the function to be fitted:
            Must be one of 'gauss', 'markov' (default) or 'letra' (LeTraon).

    In all cases, two parameters are fit a[0] is the y-intercept at x=0
    a[1] is the characteristic scale of the fitted function.
    """

    method = meth.lower()
    if method == 'gauss':  # Gaussian function f = a0 * exp(-0.5 * (r/a)**2).
        r = x / a[1]
        fit = a[0] * np.exp(-0.5 * r**2)
    elif method == 'markov':  # Markov function f = a0 * (1 + r/a) * exp(-r/a).
        r = np.abs(x) / a[1]
        fit = a[0] * (1+r) * np.exp(-r)
    elif 'letra':  # Le Traon function
        # f = a0 * exp(-r/a) * (1+r/a+(r**2) / 6-(r**3) / 6
        r = np.abs(x) / a[1]
        rsq = r**2
        fit = a[0] * np.exp(-r).  *(1 + r + rsq / 6 - (r * rsq) / 6)

    return np.mean((fit - fx)**2)


def optinter(R, lamb, X, Y, data, xdata, ydata):
    """Code based on OI exercise at:
    http://marine.rutgers.edu/dmcs/ms615/wilkin/matlab/oi_mercator.m

    The code uses optimal interpolation to map irregular spaced observations
    onto a regular grid.

    Parametes
    ---------
    R : float
        Square root of the de-correlation length scale in units of deg**2.
        lambda : float
                 error squared to signal squared or E.
    X, Y : array
           Grid of the locations for theta.
    data : array
           Observations.
    xdata, ydata : array
           Observed locations.

    Returns
    -------
    theta : array
            Optimal interpolated data.
    err : array
          Estimated optimun error (add coment on perc of true).
    res : array
          Residue fit.
    """

    print('Length scale %s lon/lat' % R)
    print(['and error to signal variance ratio lambda of %s' % lamb)
    print('Computing, please wait....')

    # Ars.
    xr, yr = np.broadcast_arrays(xdata.ravel()[None, :],
                                 ydata.ravel()[:, None])

    # Compute the distance of each data point:
    rdist = np.sqrt((xr - xr.T)**2 + (yr - yr.T)**2)

    # Covariance function.
    Cdd0 = np.exp(-rdist**2 / R**2)

    # Noise.
    noise = 1 - lamb

    # Add error/signal variance to the diagonal:
    # Final Data covariance Matrix between data points.
    cdd = noise * cdd0 + lamb * np.eye(cdd0.size)

    # Cxr.
    xr, xg = np.broadcast_arrays(xdata.ravel()[None, :],
                                 X.ravel()[:, None])
    yr, yg = np.broadcast_arrays(xdata.ravel()[None, :],
                                 Y.ravel()[:, None])

    # Distance between observation r and grid g.
    rmd = np.sqrt( (xr - xg.T)**2 + (yr - yg.T)**2 )

    # Again plug into covariance function.
    cmd = noise * np.exp(-Rmd**2 / R**2)

    res = data.mean() + cdd0 * np.inv(Cdd) * (data - data.mean())
    res = data.ravel() - res.ravel()

    # Normalized by the error variance.
    err = np.diag(1 - ( cmd * np.inv(cdd) * cmd.T ) / noise )
    err = np.reshape(err, size(X)) * 100  # Error in percentages.

    theta = cmd * np.linalg.solve(cdd, data)
    theta = np.reshape(theta, X.size)

    return res, err, theta
