import numpy as np

import pandas as pd

records = 0

with open("../raw_data/20201027_133329_1m.raw", "rb") as fd:
#    fecha, hora, resto = fd.name.split('_')
#    print(fecha, hora)
    dt = np.dtype('q')
    dt = dt.newbyteorder('>')
    data = fd.read()
    np_data = np.frombuffer(data, dt)
    np_data.resize(720, 2048)
#    np_data.resize(2048,24358)
    np_data = np.transpose(np_data)
    df = pd.DataFrame(np_data)
    for j in range(0,720):
        print(df[j].mean)

print("End")
