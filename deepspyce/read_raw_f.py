import io

import numpy as np

import pandas as pd


def raw2df(raw: io.BufferedReader,
           dtype: np.dtype = int,
           n_channels: int = 2048,
           bpcps: int = 8
           ) -> pd.DataFrame:
    """
    Funcion para convertir datos RAW a DataFrame.
    """

    # Transformamos de str(bytes) a np.array
    data = raw.read()
    dt = np.dtype(dtype).newbyteorder(">")
    np_data = np.frombuffer(data, dtype=dt)
    np_data = np.array(np_data, dtype=dtype) # ¿int64?

    # Cantidad de muestras tomadas (temporalmente)
    size = raw.tell()
    ## n_bytes / n_channels / n_bits_per_channel_per_sample
    n_records = int(size / n_channels / bpcps)
    np_data = np_data.reshape(n_channels, n_records, order='F')
    
    return pd.DataFrame(np_data)


if __name__ == "__main__":
    path = input("Please, enter your raw data path: ")
    with open(path, "rb") as raw:
        data = raw2df(raw)
    
    # This is the end
