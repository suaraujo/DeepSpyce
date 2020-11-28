import os

import numpy as np

import pandas as pd

from astropy.table import Table


# records = 0
# medias = []
# deltas = []
fc = 1420.0
bw = 100.0
freq = np.linspace(fc - bw / 2.0, fc + bw / 2.0, num=2048)

path = input("Please, enter your raw data path: ")


def raw2df(raw):
    """
    Funcion para convertir datos RAW a DataFrame
    """
    spch = 2048
    bspl = 8
    size = os.path.getsize(raw.name)
    nrec = int(size / spch / bspl)
    dt = np.dtype("q")
    dt = dt.newbyteorder(">")
    data = raw.read()
    np_data = np.frombuffer(data, dtype=dt)
    np_data = np.int64(np_data)
    np_data.resize(nrec, spch)
    np_data = np.transpose(np_data)
    df = pd.DataFrame(np_data)
#    df.columns = ['0','1']
    df = df.rename(columns = lambda x: str(x))
    return df


if __name__ == "__main__":
    fd = open(path, "rb")
    data = raw2df(fd)
    # data.to_csv("test.csv")
    print(data)
    t2 = Table.from_pandas(data)
    print(t2)
    t2.write('tabla2.fits', format='fits')
    fd.close()
# This is the end
