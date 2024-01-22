"""
Plotting with pandas is such a common use case in data science that we want to make sure
it works nicely with uniplot. Thus these tests.
"""

import pandas as pd  # type: ignore
import numpy as np  # type: ignore
import datetime 
from uniplot import plot


def test_normal_plotting():
    data = pd.DataFrame(
        data={
            "asset": ["asset1", "asset1", "asset2", "asset3"],
            "speed": [20.0, 50.0, 75.6, 12.6],
            "vertical_rms": [12.4, 23.5, 55.3, 20.5],
        }
    )
    plot(xs=data["speed"], ys=data["vertical_rms"], x_unit=" km/h", y_unit=" g")


def test_logarithmic_plotting():
    data = pd.DataFrame(
        data={
            "asset": ["asset1", "asset1", "asset2", "asset3"],
            "speed": [20.0, 50.0, 75.6, 12.6],
            "vertical_rms": [12.4, 23.5, -55.3, np.nan],
        }
    )
    plot(xs=data["speed"], ys=data["vertical_rms"])


def test_that_pandas_series_is_interpreted_as_single_dim_array():
    from uniplot.multi_series import MultiSeries

    data = pd.DataFrame(
        data={
            "asset": ["asset1", "asset1", "asset2", "asset3"],
            "speed": [20.0, 50.0, 75.6, 12.6],
            "vertical_rms": [12.4, 23.5, 55.3, 20.5],
        }
    )

    series = MultiSeries(xs=data["speed"], ys=data["vertical_rms"])
    assert not series.is_multi_dimensional


def test_grouped_plotting():
    data = pd.DataFrame(
        data={
            "asset": ["asset1", "asset1", "asset2", "asset3"],
            "speed": [20.0, 50.0, 75.6, 12.6],
            "vertical_rms": [12.4, 23.5, 55.3, 20.5],
        }
    )
    grouped_data = data.groupby("asset")
    plot(
        xs=[group["speed"] for (_, group) in grouped_data],
        ys=[group["vertical_rms"] for (_, group) in grouped_data],
        x_unit=" km/h",
        y_unit=" g",
        lines=True,
    )


def test_datetime_plotting():
    N = 100
    x = pd.date_range("2024-04-02", periods=N, freq="D")
    y = np.sin(np.linspace(0, 5 * np.pi, N))*np.cos(np.linspace(0, 7 * np.pi, N))

    plot(xs=x, ys=y, lines=True, timeseries_format="%y-%m-%d %H:%M")


def test_multi_datetime_plotting():
    # TODO! Allow different-length series in a MultiSeries,
    # so that data of different temporal resolutions can be easily plotted together.
    N = 100
    x = pd.date_range("2024-04-02", periods=N, freq="D")
    y = np.sin(np.linspace(0, 5 * np.pi, N))*np.cos(np.linspace(0, 7 * np.pi, N))

    z = pd.date_range("2024-10-30", periods=N, freq="D")
    k = np.cos(np.linspace(0, 5 * np.pi, N))*np.cos(np.linspace(0, 7 * np.pi, N))

    data = pd.DataFrame({
        "x": x,
        "y": y,
        "z": z,
        "k": k
    })

    plot(xs=[data["x"],data["z"]], ys=[data["y"], data["k"]], lines=True)