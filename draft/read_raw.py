import struct
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
records = 0

with open("../raw_data/20201027_133329_1m.raw","rb") as f:
    fecha, hora, resto,resto2 = f.name.split('_')
    print(fecha,hora)
#    dt = np.dtype('d')
    dt = np.dtype('q')
    dt = dt.newbyteorder('>')
    data = f.read()
    np_data = np.frombuffer(data,dt)
    np_data.resize(720,2048)
#    np_data.resize(2048,24358)
    np_data = np.transpose(np_data)
    df = pd.DataFrame(np_data)
#    print(np_data)
    print(df.size)
    print(df.shape)
    print(df.ndim)
    print(df[0])
    plt.plot(df[0])
    plt.yscale('log')
    plt.show()
#    for j in range(0,10):
#        plt.hist(df[j] ,bins=10)
#        plt.yscale('log')
#        plt.show()

print("End")

