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

"""Utilities for managing files."""

# =============================================================================
# IMPORTS
# =============================================================================

import io
import os

from .auxiliar import deepwarn

# ============================================================================
# CONSTANTS
# ============================================================================

rmodes = ["r", "rb"]

wmodes = ["w", "wb", "w+", "wb+", "r+"]

amodes = ["a", "ab", "a+", "ab+"]

# ============================================================================
# FUNCTIONS
# ============================================================================


def file_exists(path_str: os.PathLike):
    """Check if a file exists."""
    return os.path.isfile(path_str)


def open_file(
    path_str: os.PathLike, mode: str = "r", overwrite: bool = False
) -> io.IOBase:
    """Open a file."""
    if (mode in wmodes) and (not overwrite) and file_exists(path_str):
        raise FileExistsError("File will not be overwritten.")

    return open(path_str, mode)


def is_filelike(fileobj: io.FileIO) -> bool:
    """Check if input is a filelike object."""
    if isinstance(fileobj, (io.FileIO, io.IOBase)):
        return True
    elif hasattr(fileobj, "buffer"):
        return is_filelike(fileobj.buffer)
    elif hasattr(fileobj, "raw"):
        return is_filelike(fileobj.raw)

    return False


def get_file_attr(fileobj: io.FileIO, attr: str):
    """Get a filelike object attribute."""
    if hasattr(fileobj, attr):
        return getattr(fileobj, attr)
    if not is_filelike(fileobj):
        raise OSError("Input is not a file.")
    deepwarn(f"Unable to determine the file attribute {attr}.")

    return


def call_file_method(fileobj: io.FileIO, method: str):
    """Call a filelike object method."""
    if hasattr(fileobj, method):
        return getattr(fileobj, method)()
    if not is_filelike(fileobj):
        raise OSError("Input is not a file.")
    deepwarn(f"Unable to determine call file method {method}.")

    return


def is_opened(fileobj: io.FileIO) -> bool:
    """Check if a filelike object is opened."""
    return not get_file_attr(fileobj, "closed")


def is_writable(fileobj: io.FileIO) -> bool:
    """Check if a filelike object is writable."""
    return call_file_method(fileobj, "writable")


def is_readable(fileobj: io.FileIO) -> bool:
    """Check if a filelike object is readable."""
    return call_file_method(fileobj, "readable")


def close_file(fileobj: io.FileIO):
    """Close a file."""
    return call_file_method(fileobj, "close")


def read_file(path_or_stream: os.PathLike, mode: str = "r") -> str:
    """Read a file."""
    if isinstance(path_or_stream, (str, os.PathLike)):
        with open_file(path_or_stream, mode) as buff:
            data = buff.read()
        return data
    if is_readable(path_or_stream):
        return path_or_stream.read()

    raise OSError(f"Could not read {path_or_stream}")


def write_to_file(
    path_or_stream: os.PathLike,
    data: any = None,
    mode: str = "w",
    overwrite: bool = False,
) -> None:
    """Write data into a file."""
    if data is None:
        return
    if isinstance(path_or_stream, (str, os.PathLike)):
        with open_file(path_or_stream, mode, overwrite) as buff:
            buff.write(data)
        return
    if is_writable(path_or_stream):
        path_or_stream.write(data)
        return

    raise OSError(f"Could not write data into {path_or_stream}")
