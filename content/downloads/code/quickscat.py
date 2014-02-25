"""
Module for reading and verifying RSS gridded binary data files.

Remote Sensing Systems
444 Tenth Street, Suite 200
Santa Rosa, CA 95401, USA
FTP: ftp://ftp.ssmi.com
Web: http://www.remss.com
Support: support@remss.com
Terms of Data Use:
http://www.remss.com/terms_of_data_use/terms_of_data_use.html
"""

import sys
import copy
import gzip
import decimal
import numpy as np
from operator import mul
from functools import reduce
from collections import namedtuple
from collections import OrderedDict


class Dataset(object):
    """Base class for bytemap datasets.
    Public data:
        filename = name of data file
        missing = fill value used for missing data;
                  if None, then fill with byte codes (251-255)
        dimensions = dictionary of dimensions for each coordinate
        variables = dictionary of data for each variable

    All classes derived from Dataset must implement the following:
        _attributes() = returns list of attributes for each variable (list)
        _coordinates() = returns coordinates (tuple)
        _shape() = returns shape of raw data (tuple)
        _variables() = returns list of all variables to get (list)

    The derived class must provide "_get_" methods for the attributes.

    If the derived class provides "_get_" methods for the variables,
    those methods receive first priority.

    The "_get_" methods in this module receive second priority.

    The last priority is "_default_get", which requires:
        _get_index(var) = returns bmap index for var
        _get_scale(var) = returns bmap scale for var
        _get_offset(var) = returns bmap offset for var
    """

    def __init__(self):
        self.dimensions = self._get_dimensions()
        self.variables = self._get_variables()

    def _default_get(self, var, bmap):
        data = get_data(bmap, self._get_index(var))
        acopy = copy.deepcopy(data)
        bad = is_bad(data)
        try:
            data *= self._get_scale(var)
        except _NoValueFound:
            pass
        try:
            data += self._get_offset(var)
        except _NoValueFound:
            pass
        if not self.missing:
            data[bad] = acopy[bad]
        else:
            data[bad] = self.missing
        return data

    def _dtype(self):
        return np.uint8

    def _get(self, var):
        try:
            return _get_(var, _from_=self)
        except _NoMethodFound:
            pass
        try:
            return _get_(var, _from_=thismodule())
        except _NoMethodFound:
            pass
        return self._default_get

    def _get_avariable(self, var, data):
        variable = self._get(var)(var, data)
        return Variable(var, variable, self)

    def _get_coordinates(self, var=None):
        if not var:
            return self._coordinates()
        if var in self._coordinates():
            return (var,)
        return tuple([c for c in self._coordinates() if c != 'variable'])

    def _get_dimensions(self):
        dims = OrderedDict(list(zip(self._coordinates(), self._shape())))
        del dims['variable']
        return dims

    def _get_variables(self):
        data = OrderedDict()
        try:
            stream = readgz(self.filename)
        except:
            return data
        bmap = unpack(stream, shape=self._shape(), dtype=self._dtype())
        for var in self._variables():
            data[var] = self._get_avariable(var, bmap)
        return data


def readgz(filename):
    with gzip.open(filename, 'rb') as f:
        stream = f.read()
    return stream


def thismodule():
    return sys.modules[__name__]


def unpack(stream, shape, dtype):
    count = reduce(mul, shape)
    return np.fromstring(stream, dtype=dtype, count=count).reshape(shape)


"""Library of Methods for _get_ Functions:"""


def btest(ival, ipos):
    """Same usage as Fortran btest function."""
    return (ival & (1 << ipos)) != 0


def cosd(x):
    return np.cos(np.radians(x))


def get_data(bmap, indx, dtype=np.float64):
    """Return numpy array of dytpe for the variable in bmap given by indx."""
    return np.array(np.squeeze(bmap[..., indx, :, :]), dtype=dtype)


def get_uv(speed, direction):
    """
    Given speed and direction (degrees oceanographic),
    return u (zonal) and v (meridional) components.
    """
    u = speed * sind(direction)
    v = speed * cosd(direction)
    return u, v


def ibits(ival, ipos, ilen):
    """Same usage as Fortran ibits function."""
    ones = ((1 << ilen)-1)
    return (ival & (ones << ipos)) >> ipos


def is_bad(bmap, maxvalid=250):
    """Return mask where data are bad."""
    return bmap > maxvalid


def sind(x):
    return np.sin(np.radians(x))

where = np.where


"""Library of Named Exceptions:"""

_NoMethodFound = AttributeError

_NoValueFound = (AttributeError, KeyError)

_NotFound = AttributeError


"""Library of Named _get_ Functions:"""


def _get_(var, _from_):
    return getattr(_from_, '_get_%s' % var)


def _get_ice(var, bmap, indx=0, icevalue=252):
    return get_data(bmap, indx, dtype=bmap.dtype) == icevalue


def _get_land(var, bmap, indx=0, landvalue=255):
    return get_data(bmap, indx, dtype=bmap.dtype) == landvalue


def _get_latitude(var, bmap, nlat=720, dlat=0.25, lat0=-89.875):
    if np.shape(bmap)[-2] != nlat:
        sys.exit('Latitude mismatch')
    return np.array([dlat*ilat + lat0 for ilat in range(nlat)])


def _get_longitude(var, bmap, nlon=1440, dlon=0.25, lon0=0.125):
    if np.shape(bmap)[-1] != nlon:
        sys.exit('Longitude mismatch')
    return np.array([dlon*ilon + lon0 for ilon in range(nlon)])


def _get_nodata(var, bmap, indx=0):
    return is_bad(get_data(bmap, indx, dtype=bmap.dtype))


class Variable(np.ndarray):
    """Variable exists solely to subclass numpy array with attributes."""

    def __new__(cls, var, data, dataset):
        obj = np.asarray(data).view(cls)
        for attr in dataset._attributes():
            get = _get_(attr, _from_=dataset)
            setattr(obj, attr, get(var))
        return obj


OneOb = namedtuple('OneOb', 'lon lat asc val ndp')
"""
OneOb corresponds to one observation from verify file with:
    lon = longitude index
    lat = latitude index
    asc = ascending/descending index
    val = verify value
    ndp = number of decimal places given in verify
    The (asc,lat,lon) indices are 0-based.
"""


def places(astring):
    """
    Given a string representing a floating-point number,
    return number of decimal places of precision (note: is negative).
    """
    return decimal.Decimal(astring).as_tuple().exponent


def readtext(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines


def tokenize(line):
    return [item.strip() for item in line.split()]


def zerobased(indx):
    return indx - 1


class QuikScatDaily(Dataset):
    """Read daily QSCAT bytemaps.
    Public data:
        filename = name of data file
        missing = fill value used for missing data;
                  if None, then fill with byte codes (251-255)
        dimensions = dictionary of dimensions for each coordinate
        variables = dictionary of data for each variable

    This routine will read RSS scatterometer daily bytemap files.
    reads version-4 files released April 2011

    The routine reads the quikscat file and similar to a netCDF file provides
    the contents and variable attributes:
    'mingmt' : 'Minute of Day UTC',
    'windspd' : '10-m Surface Wind Speed in m/s',
    'winddir' : '10-m Surface Wind Direction', degrees the wind is blowing to,
                North = 0 deg
    'scatflag' : 'Scatterometer Rain Flag', 0=no rain, 1=rain
    'radrain' : 'Radiometer Rain Flag', collocated radiometer columnar rain
                rate in km*mm/hr
                this is found using an SSMI or TMI observation within 60
                minutes of the scat obs.
        radrain contains -999. where there is no collocated radiometer data
                            0. where there is radiometer data, but there is no
                               measurable rain
                           -1. where there is radiometer data, no measurable
                               rain, but nearby cells have rain
                            0.5 to 31.0  km*mm/hr radiometer columnar rain
                                         rate for that cell
    'longitude' : 'Grid Cell Center Longitude',
    'latitude' : 'Grid Cell Center Latitude',
    'land' : 'Is this land?',
    'ice' : 'Is this ice?',
    'nodata' : 'Is there no data?'

    The center of the first cell of the 1440 column and 720 row map is at
    0.125 E longitude and -89.875 latitude.
    The center of the second cell is 0.375 E longitude, -89.875 latitude.
        real lat = 0.25 * cell y position -90.125
        real lon = 0.25 * cell x position -0.125

    please read the description file on www.remss.com for information on the
    various fields, or contact RSS support:  http://www.remss.com/support

    program created for quikscat  Aug 2013
    """

    def __init__(self, filename, missing=-999.):
        """
        Required arguments:
            filename = name of data file to be read (string)

        Optional arguments:
            missing = fill value for missing data,
                      default is the value used in verify file
        """
        self.filename = filename
        self.missing = missing
        Dataset.__init__(self)

    def _attributes(self):
        return ['coordinates', 'long_name', 'units', 'valid_min', 'valid_max']

    def _coordinates(self):
        return ('orbit_segment', 'variable', 'latitude', 'longitude')

    def _shape(self):
        return (2, 4, 720, 1440)

    def _variables(self):
        return ['mingmt', 'windspd', 'winddir', 'scatflag', 'radrain',
                'longitude', 'latitude', 'land', 'ice', 'nodata']

    def _get_index(self, var):
        return {'windspd': 1,
                'winddir': 2,
                'rain': 3,
                }[var]

    def _get_scale(self, var):
        return {'mingmt': 6.0,
                'windspd': 0.2,
                'winddir': 1.5,
                }[var]

    def _get_long_name(self, var):
        return {'mingmt': 'Minute of Day UTC',
                'windspd': '10-m Surface Wind Speed',
                'winddir': '10-m Surface Wind Direction',
                'scatflag': 'Scatterometer Rain Flag',
                'radrain': 'Radiometer Rain Flag',
                'longitude': 'Grid Cell Center Longitude',
                'latitude': 'Grid Cell Center Latitude',
                'land': 'Is this land?',
                'ice': 'Is this ice?',
                'nodata': 'Is there no data?',
                }[var]

    def _get_units(self, var):
        return {'mingmt': 'minute of day',
                'windspd': 'm/s',
                'winddir': 'deg oceanographic',
                'scatflag': '0=no-rain, 1=rain',
                'radrain': '0=no-rain, -1=adjacent rain, >0=rain(km*mm/hr)',
                'longitude': 'degrees east',
                'latitude': 'degrees north',
                'land': 'True or False',
                'ice': 'True or False',
                'nodata': 'True or False',
                }[var]

    def _get_valid_min(self, var):
        return {'mingmt': 0.0,
                'windspd': 0.0,
                'winddir': 0.0,
                'scatflag': 0,
                'radrain': -1,
                'longitude': 0.0,
                'latitude': -90.0,
                'land': False,
                'ice': False,
                'nodata': False,
                }[var]

    def _get_valid_max(self, var):
        return {'mingmt': 1440.0,
                'windspd': 50.0,
                'winddir': 360.0,
                'scatflag': 1,
                'radrain': 31,
                'longitude': 360.0,
                'latitude': 90.0,
                'land': True,
                'ice': True,
                'nodata': True,
                }[var]

    def _get_mingmt(self, var, bmap):
        mingmt = get_data(bmap, indx=0)
        mingmt *= self._get_scale(var)
        return mingmt

    def _get_scatflag(self, var, bmap):
        indx = self._get_index('rain')
        scatflag = get_data(ibits(bmap, ipos=0, ilen=1), indx=indx)
        bad = is_bad(get_data(bmap, indx=0))
        scatflag[bad] = self.missing
        return scatflag

    def _get_radrain(self, var, bmap):
        indx = self._get_index('rain')
        radrain = get_data(ibits(bmap, ipos=1, ilen=1), indx=indx)
        good = (radrain == 1)
        radrain[~good] = self.missing
        intrain = get_data(ibits(bmap, ipos=2, ilen=6), indx=indx)
        nonrain = where(intrain == 0)
        adjrain = where(intrain == 1)
        hasrain = where(intrain > 1)
        intrain[nonrain] = 0.0
        intrain[adjrain] = -1.0
        intrain[hasrain] = 0.5 * (intrain[hasrain]-1)
        radrain[good] = intrain[good]
        bad = is_bad(get_data(bmap, indx=0))
        radrain[bad] = self.missing
        return radrain


class QuikScatAveraged(Dataset):
    """ Read averaged QSCAT bytemaps.
    Public data:
        filename = name of data file
        missing = fill value used for missing data;
                  if None, then fill with byte codes (251-255)
        dimensions = dictionary of dimensions for each coordinate
        variables = dictionary of data for each variable

    This subroutine will read RSS scatterometer time-averaged bytemap files.
    reads version-4 files released April 2011

    The routine reads the quikscat file and similar to a netCDF file provides
    the contents and variable attributes:
    'windspd' : '10-m Surface Wind Speed in m/s',
    'winddir' : '10-m Surface Wind Direction', degrees the wind is blowing to,
                North = 0 deg
    'scatflag' : 'Scatterometer Rain Flag', 0=no rain, 1=rain
    'radrain' : 'Radiometer Rain Flag', collocated radiometer columnar rain
                rate in km*mm/hr this is found using an SSMI or TMI
                observation within 60 minutes of the scat obs.
        radrain contains -999. where there is no collocated radiometer data
                            0. where there is radiometer data, but there is no
                               measurable rain
                           -1. where there is radiometer data, no measurable
                               rain, but nearby cells have rain
                            0.5 to 31.0  km*mm/hr radiometer columnar rain
                                         rate for that cell
    'longitude' : 'Grid Cell Center Longitude',
    'latitude' : 'Grid Cell Center Latitude',
    'land' : 'Is this land?',
    'ice' : 'Is this ice?',
    'nodata' : 'Is there no data?'

    The center of the first cell of the 1440 column and 720 row map is at
    0.125 E longitude and -89.875 latitude.  The center of the second cell is
    0.375 E longitude, -89.875 latitude.
        real lat = 0.25 * cell y position -90.125
        real lon = 0.25 * cell x position -0.125

    please read the description file on www.remss.com for information on the
    various fields, or contact RSS support:  http://www.remss.com/support

    program created for quikscat  Aug 2013
    """

    def __init__(self, filename, missing=-999.):
        """
        Required arguments:
            filename = name of data file to be read (string)

        Optional arguments:
            missing = fill value for missing data,
                      default is the value used in verify file
        """
        self.filename = filename
        self.missing = missing
        Dataset.__init__(self)

    def _attributes(self):
        return ['coordinates', 'long_name', 'units', 'valid_min', 'valid_max']

    def _coordinates(self):
        return ('variable', 'latitude', 'longitude')

    def _shape(self):
        return (3, 720, 1440)

    def _variables(self):
        return ['windspd', 'winddir', 'scatflag', 'radrain',
                'longitude', 'latitude', 'land', 'ice', 'nodata']

    # _default_get():
    def _get_index(self, var):
        return {'windspd': 0,
                'winddir': 1,
                'rain': 2}[var]

    def _get_scale(self, var):
        return {'windspd': 0.2,
                'winddir': 1.5}[var]

    def _get_long_name(self, var):
        return {'windspd': '10-m Surface Wind Speed',
                'winddir': '10-m Surface Wind Direction',
                'scatflag': 'Scatterometer Rain Flag',
                'radrain': 'Radiometer Rain Flag',
                'longitude': 'Grid Cell Center Longitude',
                'latitude': 'Grid Cell Center Latitude',
                'land': 'Is this land?',
                'ice': 'Is this ice?',
                'nodata': 'Is there no data?',
                }[var]

    def _get_units(self, var):
        return {'windspd': 'm/s',
                'winddir': 'deg oceanographic',
                'scatflag': '0=no-rain, 1=rain',
                'radrain': '0=no-rain, -1=adjacent rain, >0=rain(km*mm/hr)',
                'longitude': 'degrees east',
                'latitude': 'degrees north',
                'land': 'True or False',
                'ice': 'True or False',
                'nodata': 'True or False',
                }[var]

    def _get_valid_min(self, var):
        return {'windspd': 0.0,
                'winddir': 0.0,
                'scatflag': 0,
                'radrain': -1,
                'longitude': 0.0,
                'latitude': -90.0,
                'land': False,
                'ice': False,
                'nodata': False,
                }[var]

    def _get_valid_max(self, var):
        return {'windspd': 50.0,
                'winddir': 360.0,
                'scatflag': 1,
                'radrain': 31,
                'longitude': 360.0,
                'latitude': 90.0,
                'land': True,
                'ice': True,
                'nodata': True,
                }[var]

    def _get_scatflag(self, var, bmap):
        indx = self._get_index('rain')
        scatflag = get_data(ibits(bmap, ipos=0, ilen=1), indx=indx)
        bad = is_bad(get_data(bmap, indx=0))
        scatflag[bad] = self.missing
        return scatflag

    def _get_radrain(self, var, bmap):
        indx = self._get_index('rain')
        radrain = get_data(ibits(bmap, ipos=1, ilen=1), indx=indx)
        good = (radrain == 1)
        radrain[~good] = self.missing
        intrain = get_data(ibits(bmap, ipos=2, ilen=6), indx=indx)
        nonrain = where(intrain == 0)
        adjrain = where(intrain == 1)
        hasrain = where(intrain > 1)
        intrain[nonrain] = 0.0
        intrain[adjrain] = -1.0
        intrain[hasrain] = 0.5*(intrain[hasrain]-1)
        radrain[good] = intrain[good]
        bad = is_bad(get_data(bmap, indx=0))
        radrain[bad] = self.missing
        return radrain
