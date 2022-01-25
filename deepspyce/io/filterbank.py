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

"""Module with .fil I/O functions."""

# =============================================================================
# IMPORTS
# =============================================================================

import os
import struct
from datetime import datetime

from deepspyce.utils.auxiliar import data_to_bytes, deepwarn
from deepspyce.utils.files_utils import (
    get_file_attr,
    is_filelike,
    read_file,
    write_to_file,
)

import numpy as np

import pandas as pd

from .iar import read_iar

# ============================================================================
# FUNCTIONS
# ============================================================================


def _iardict_to_fil_header(iardict: dict) -> dict:
    """Build dict header from dict iar."""
    source_name = iardict["Source Name"]
    source_ra = iardict["Source RA (hhmmss.s)"]
    source_dec = iardict["Source DEC (ddmmss.s)"]
    # ref_dm = iardict["Reference DM"]
    # pul_period = iardict["Pulsar Period"]
    # high_freq = iardict["Highest Observation Frequency (MHz)"]
    telescope_id = int(iardict["Telescope ID"])
    machine_id = int(iardict["Machine ID"])
    data_type = int(iardict["Data Type"])
    # observing_time = int(iardict["Observing Time (minutes)"])
    # gain = iardict["Gain (dB)"]
    # bandwidth = int(iardict["Total Bandwith (MHz)"])
    avg_data = int(iardict["Average Data"])
    sub_bands = int(iardict["Sub Bands"])

    # ---- ROACH ----
    # values
    fft_pts = 128
    adc_clk = 200e6
    #  parameters
    tsamp = avg_data * fft_pts / adc_clk
    f_off = adc_clk / fft_pts * 1e-6

    time_now = datetime.now().strftime("_%Y%m%d_%H%M%S")

    # tsamp = 1e6 / float(bandwidth) * avg_data
    rawdatafile = f"ds{avg_data}_{source_name}{time_now}.fil"

    return {
        "telescope_id": telescope_id,
        "machine_id": machine_id,
        "data_type": data_type,
        "rawdatafile": rawdatafile,
        "source_name": source_name,
        "az_start": 0.0,
        "za_start": 0.0,
        "src_raj": source_ra,
        "src_dej": source_dec,
        "tstart": 0.0,
        "tsamp": tsamp,
        "fch1": 0.0,
        "foff": f_off,
        "nchans": sub_bands,
        "nifs": 1,
        "ibeam": 1,
        "nbeams": 1,
    }


def _check_key_pos(
    header: dict, key: str, pos: int, verb: bool = False
) -> bool:
    keys = list(header.keys())
    loc = keys.index(key) if key in keys else None
    if loc == pos:
        return True
    if loc is None:
        if verb:
            deepwarn(f"{key} is missing in the header.")
        return None
    if verb:
        deepwarn(f"{key} is not in the {pos} header key.")

    return False


def check_header_start_end(header: dict, verb: bool = False) -> tuple:
    """Check the HEADER_START and HEADER_END entries of the header."""
    start = _check_key_pos(header, "HEADER_START", 0, verb)
    end = _check_key_pos(header, "HEADER_END", len(header) - 1, verb)
    if start and (header["HEADER_START"] is not None):
        if verb:
            deepwarn("header['HEADER_START'] should be None!")
        start = False
    if end and (header["HEADER_END"] is not None):
        if verb:
            deepwarn("header['HEADER_END'] should be None!")
        end = False
    if (start and end) and verb:
        print("HEADER_START and HEADER END are OK!.")

    return (start, end)


def fixed_header_start_end(header: dict, check: bool = True) -> dict:
    """Fix the HEADER_START and HEADER_END entries of the header."""
    if check:
        start, end = check_header_start_end(header, False)
        if start and end:
            return header
    hs = "HEADER_START"
    he = "HEADER_END"
    fixedheader = dict({hs: None})
    for key, value in header.items():
        if key not in [hs, he]:
            fixedheader[key] = value
    fixedheader[he] = None

    return fixedheader


def _encode_header(hedicc: dict) -> bytes:

    bina = b""
    for key, value in hedicc.items():
        ret = struct.pack("I", len(key)) + key.encode()
        if value is not None:
            if isinstance(value, str):
                ret = ret + struct.pack("I", len(value)) + value.encode()
            elif isinstance(value, int):
                ret = ret + struct.pack("<l", value)
            else:
                ret = ret + struct.pack("<d", value)
        bina = bina + ret

    return bina


def iar_to_fil_header(iar, encode: bool = False) -> bytes:
    """Transform .iar data to header."""
    if not isinstance(iar, dict):
        iar = read_iar(iar)
    head = _iardict_to_fil_header(iar)
    if not encode:
        return head
    head = fixed_header_start_end(head)

    return _encode_header(head)


def _binraw_to_filterbank(
    bin_raw: bytes,
    headerdict: dict = None,
    outfile: os.PathLike = None,
    overwrite: bool = False,
) -> None:
    """Generate .fil file from header dict and raw file."""
    if headerdict is None:
        headerdict = dict()
    if not isinstance(headerdict, dict):
        headerdict = dict(headerdict)
    name = headerdict.get("rawdatafile")
    if outfile is None:
        if name is None:
            raise OSError("Could not resolve/infer output file name.")
        else:
            outfile = name
            filen = outfile
    elif is_filelike(outfile):
        filen = get_file_attr(outfile, "name")
    else:
        filen = os.path.basename(outfile)
    if filen != name:
        deepwarn(
            f"\nFile name: '{filen}' and "
            + f"\nrawdatafile: '{name}' in header "
            + "\ndo not match."
        )
    headerdict = fixed_header_start_end(headerdict)
    bin_header = _encode_header(headerdict)
    write_to_file(outfile, bin_header, "wb", overwrite)
    write_to_file(outfile, bin_raw, "ab")

    return


def raw_to_filterbank(
    rawfile: os.PathLike,
    header: dict = None,
    outfile: os.PathLike = None,
    overwrite: bool = False,
) -> None:
    """Generate .fil file from header dict and raw data file."""
    bin_raw = read_file(rawfile, "rb")
    _binraw_to_filterbank(bin_raw, header, outfile, overwrite)

    return


def df_to_filterbank(
    df: pd.DataFrame,
    header: dict = None,
    outfile: os.PathLike = None,
    overwrite: bool = False,
    fmt: np.dtype = ">i8",
    order: str = "F",
) -> None:
    """Generate .fil file from dataframe and header dict."""
    bin_raw = data_to_bytes(df, fmt, order)
    _binraw_to_filterbank(bin_raw, header, outfile, overwrite)

    return
