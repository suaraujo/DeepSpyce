import numpy as np
import pandas as pd
import struct as stc
import io

np.random.seed(42)
df=pd.DataFrame(np.random.randint(0, 100000, size=(1, 2048)))
print(df.transpose())

# este seria la parte del data_raw
a=df.to_numpy(dtype='float64')
#print(a.dtype)

a=a.flatten()

#print(a.dtype)
#print(a)
cant=len(a)


raw3 = stc.pack('d'*cant,*a)

#aca con el que pasa el file

fd1= io.BytesIO()
fd1.write(raw3)



def raw2df(raw):
    """
    Funcion para convertir datos RAW a DataFrame
    """
    spch = 2048
    bspl = 8
    raw.seek(0)
    data = raw.read()
    size = raw.tell()
    nrec = int(size / spch / bspl)
    dt = np.dtype("q")
    dt = dt.newbyteorder(">")

    np_data = np.frombuffer(data, dtype=dt)
    np_data = np.int64(np_data)
    np_data.resize(nrec, spch)
    np_data = np.transpose(np_data)
    df = pd.DataFrame(np_data)
    return df


if __name__ == "__main__":
    #fd = open(' ', "rb")
    data = raw2df(fd1)
    print(data)
    # data.to_csv("test.csv")
    #fd.close()
# This is the end

