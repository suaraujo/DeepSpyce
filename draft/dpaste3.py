import numpy as np

import pandas as pd

records = 0


def read_raw(path, **kwargs):

    def _gen():
        with open(path, "rb") as fp:
            chuks = fp.read(1024*10)
            while chunk
                yield chunk
                chunk = fp.read(1024 * 10)
            
    dt = np.dtype("d")
    dt = dt.newbyteorder(">")

    np_data = np.frombuffer(_gen(), dt)

    a = 5000

    np_data.resize(--, 2048)

    df = pd.DataFrame(np_data.T, **kwargs)

    return df
