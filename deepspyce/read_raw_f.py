import io

import numpy as np
import pandas as pd
from astropy.io import fits


def raw2df(
    raw: io.BufferedReader,
    dtype: np.dtype = int,
    n_channels: int = 2048,
    bpcps: int = 8,
) -> pd.DataFrame:
    """
    Función para convertir datos RAW a DataFrame.
    """

    # Transformamos de str(bytes) a np.array
    data = raw.read()
    dt = np.dtype(dtype).newbyteorder(">")
    np_data = np.frombuffer(data, dtype=dt)
    np_data = np.array(np_data, dtype=dtype)  # ¿int64?

    # Cantidad de muestras tomadas (temporalmente)
    size = raw.tell()
    # n_bytes / n_channels / n_bits_per_channel_per_sample
    n_records = int(size / n_channels / bpcps)
    np_data = np_data.reshape(n_channels, n_records, order="F")

    return pd.DataFrame(np_data)


def df2fits(
    data: pd.DataFrame, name: str = "test.fits", overwrite: bool = True,
) -> None:
    """
    Función para crear archivo FITS desde DataFrame.
    """

    hdr = fits.Header()
    # Incluí parte del sample Header de TREG_091209.cal.acs.txt,
    # de Single Dish FITS (SDFITS)
    hdr["SIMPLE"] = ("T", "/ conforms to FITS standard")
    hdr["BITPIX"] = (8, "/ conforms to FITS standard")
    hdr["NAXIS"] = (0, "/ number of array dimensions")
    hdr["EXTEND"] = ("T", "/File contains extensions")
    hdr["DATE"] = ("2010-06-15", "/")
    hdr["ORIGIN"] = ("IAR", "/ origin of observation")
    hdr["TELESCOP"] = ("Antena del IAR", "/ the telescope used")
    hdr["GUIDEVER"] = (
        "DeepSpyce ver1.0",
        "/ this file was created by DeepSpyce",
    )
    hdr["FITSVER"] = ("1.6", "/ FITS definition version")

    # -----------------------------------------------------------------------
    primary_hdu = fits.PrimaryHDU(data, header=hdr)
    # primary_hdu = fits.BinTableHDU(data, header=hdr, character_as_bytes=True)
    # BinTable tira error: TypeError: Table data has incorrect type.
    hdul = fits.HDUList([primary_hdu])
    hdul.writeto(name, overwrite=overwrite)

    return


if __name__ == "__main__":
    path = input("Please, enter your raw data path: ")
    with open(path, "rb") as raw:
        data = raw2df(raw)
    df2fits(data)

    # This is the end
