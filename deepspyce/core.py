#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   DeepSpyce Project (https://github.com/suaraujo/DeepSpyce).
# Copyright (c) 2020, Susana Beatriz Araujo Furlan
# License: MIT
#   Full Text: https://github.com/suaraujo/DeepSpyce/blob/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Module with core functions."""

# =============================================================================
# IMPORTS
# =============================================================================

import io
from datetime import datetime

from astropy.io import fits

import numpy as np

import pandas as pd

# ============================================================================
# FUNCTIONS
# ============================================================================


def raw2df(
    raw: io.BufferedReader,
    n_channels: int = 2048,
    fmt: np.dtype = ">i8",
    order: str = "F",
) -> pd.DataFrame:
    """Convert raw data to dataframe."""
    # Transformamos de str(bytes) a np.array
    data = raw.read()
    dt = np.dtype(fmt)
    np_data = np.array(np.frombuffer(data, dtype=dt))
    bytes_per_data = dt.alignment
    total_bytes = raw.tell()
    n_records = int(total_bytes / n_channels / bytes_per_data)
    np_data = np_data.reshape(n_channels, n_records, order=order)

    return pd.DataFrame(np_data)


def df2fits(
    data: pd.DataFrame, filename: str = "test.fits", overwrite: bool = True
) -> None:
    """Create .fits from dataframe."""
    # Sample: TREG_091209.cal.acs.txt [Single Dish FITS (SDFITS)]
    hdr = fits.Header()
    hdr["SIMPLE"] = ("T", "/ conforms to FITS standard")
    hdr["BITPIX"] = (8, "/ BITS/PIXEL")
    hdr["NAXIS"] = (0, "/ number of array dimensions")
    hdr["EXTEND"] = ("T", "/File contains extensions")
    hdr["DATE"] = (datetime.today().strftime("%y-%m-%d"), "/")
    hdr["ORIGIN"] = ("IAR", "/ origin of observation")
    hdr["TELESCOP"] = ("Antena del IAR", "/ the telescope used")
    # hdr["OBSERVAT"] = ("IAR", "/ the observatory")
    hdr["GUIDEVER"] = (
        "DeepSpyce ver1.0",
        "/ this file was created by DeepSpyce",
    )
    hdr["FITSVER"] = ("1.6", "/ FITS definition version")

    primary_hdu = fits.PrimaryHDU(data, header=hdr)
    hdul = fits.HDUList([primary_hdu])
    hdul.writeto(filename, overwrite=overwrite)

    return


if __name__ == "__main__":
    path = input("Please, enter your raw data path: ")
    with open(path, "rb") as raw:
        data = raw2df(raw)
    df2fits(data)

    # This is the end
