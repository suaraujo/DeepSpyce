import numpy as np

import pandas as pd

records = 0

with open("../datos/20201027_133329_data.raw","rb") as f:
    fecha, hora, resto = f.name.split('_')
    print(fecha,hora)
    dt = np.dtype('d')
    dt = dt.newbyteorder('>')
    data = f.read()
    np_data = np.frombuffer(data,dt)
    np_data.resize(5000,2048)
#    np_data.resize(2048,24358)
    np_data = np.transpose(np_data)
    df = pd.DataFrame(np_data)

print("End")

