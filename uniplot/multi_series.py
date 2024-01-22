import numpy as np
from numpy.typing import NDArray

import datetime
import pendulum
import pandas as pd
from typing import List


class MultiSeries:
    """
    A `MultiSeries` is an object that contains multiple series of numeric values in both x and y direction.

    If no `xs` parameter is supplied, then we generate x axis values as a serial index integer value.
    """

    def __init__(self, ys, xs=None) -> None:
        # Init types
        self.xs: List[NDArray] = []
        self.ys: List[NDArray] = []

        # First check if the input is multi-dim
        self.is_multi_dimensional: bool = _is_multi_dimensional(ys)

        # Initialize y series
        if self.is_multi_dimensional:
            self.ys = [_cast_as_numpy_floats(ys_row) for ys_row in ys]
        else:
            self.ys = [_cast_as_numpy_floats(ys)]

        # Initialize x series, first checking if it is a datetime-ish series
        self.x_is_timeseries: bool = _is_timeseries_ish(xs)

        if xs is None:
            self.xs = [
                np.arange(1, len(ys_row) + 1, step=1, dtype=int) for ys_row in self.ys
            ]
        else:
            if self.is_multi_dimensional:
                if self.x_is_timeseries:
                    self.xs = [_convert_timeseries_to_numpy(xs_row) for xs_row in xs]
                else:
                    self.xs = [_cast_as_numpy_floats(xs_row) for xs_row in xs]
            else:
                if self.x_is_timeseries:
                    self.xs = [_convert_timeseries_to_numpy(xs)]
                else:
                    self.xs = [_cast_as_numpy_floats(xs)]

    def __len__(self) -> int:
        """Return the number of time series."""
        return len(self.ys)

    def shape(self) -> List[int]:
        """Return a list with the length of the time series."""
        return [len(ys_row) for ys_row in self.ys]

    def set_x_axis_to_log10(self) -> None:
        """Apply log10 to all x series.
        Raises a `ValueError` if any the x-axis is timeseries.
        """
        if self.x_is_timeseries:
            raise ValueError("Cannot format a timeseries as logarithmic.")

        self.xs = [_safe_log10(x) for x in self.xs]

    def set_y_axis_to_log10(self) -> None:
        """Apply log10 to all y series."""
        self.ys = [_safe_log10(y) for y in self.ys]

    def y_max(self) -> float:
        return max([_safe_max(ys_row) for ys_row in self.ys])

    def y_min(self) -> float:
        return min([_safe_min(ys_row) for ys_row in self.ys])

    def x_max(self) -> float:
        return max([_safe_max(xs_row) for xs_row in self.xs])

    def x_min(self) -> float:
        return min([_safe_min(xs_row) for xs_row in self.xs])


###########
# private #
###########


def _is_multi_dimensional(series) -> bool:
    """
    Check if the object is multi-dimensional.

    Ref.: https://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-an-object-is-iterable
    """
    try:
        [iter(x) for x in series]
    except TypeError:
        return False
    else:
        return True


def _is_timeseries_ish(series) -> bool:
    """
    Check if the object is datetime-like.
    This might be a pandas DateTime, a list of datetimes, or a list of date(s).
    """
    if isinstance(series, pd.DatetimeIndex):
        return True
    elif isinstance(series, pd.Series):
        return series.dtype == 'datetime64[ns]'
    elif isinstance(series, list):
        if all(isinstance(x, datetime.date) for x in series):
            return True
        elif all(isinstance(x, datetime.datetime) for x in series):
            return True
        elif isinstance(series, pendulum.DateTime):
            return True

    return False


def _convert_timeseries_to_numpy(series) -> NDArray:
    """
    Converts to a numpy floating-point array, of unix epoch timestamps,
    with nano-second precision.
    """
    # first, convert to pandas datetime
    if isinstance(series, pd.Series):
        series = pd.to_datetime(series)
    elif isinstance(series, pd.DatetimeIndex):
        series = pd.to_datetime(series.to_series())
    elif isinstance(series, list):
        series = pd.to_datetime(pd.Series(series))
    
    # then, convert each Timestamp to a unix epoch timestamp
    series = series.astype(np.int64) // 10 ** 9

    # finally, convert to numpy array
    return series.values


def _cast_as_numpy_floats(array) -> NDArray:
    """
    Attempts to make a numeric NumPy array from enumerable input.

    If simply casting into a NumPy array yields one of `numpy.inexact`
    floating-point type, it returns the array. Otherwise, it attempts to cast
    it as NumPy float.
    """
    numpy_array = np.array(array)

    if np.issubdtype(numpy_array.dtype, np.inexact):
        return numpy_array

    # If it not already intitializes as a numeric type, then all we can do is
    # attempt to cast to float (including NaNs)
    return numpy_array.astype(float)


def _safe_max(array) -> float:
    return array[~np.isnan(array)].max()


def _safe_min(array) -> float:
    return array[~np.isnan(array)].min()


def _safe_log10(x: NDArray) -> NDArray:
    x = x.astype(float)
    x[x <= 0.0] = np.nan
    return np.log10(x)
