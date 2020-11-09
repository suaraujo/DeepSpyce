import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statistics as st

records = 0
medias = []
deltas = []

with open("../../dirtest/20201027_133329_0.raw", "rb") as fd:
#with open("../raw_data/20201027_133329_1m.raw", "rb") as fd:
#    fecha, hora, resto = fd.name.split('_')
#    print(fecha, hora)
    dt = np.dtype('q')
    dt = dt.newbyteorder('>')
    data = fd.read()
    np_data = np.frombuffer(data, dt)
#    np_data.resize(720, 2048)
    np_data.resize(24358,2048)
    np_data = np.transpose(np_data)
    df = pd.DataFrame(np_data)
    for j in range(0,720):
        medias.append(df[j].mean())
        deltas.append(np.abs(df[j].mean() - 16288))

plt.hist(medias, bins=20)
plt.show()
plt.hist(deltas, bins=20)
plt.show()
print(st.mean(medias), st.stdev(medias))
print("End")
