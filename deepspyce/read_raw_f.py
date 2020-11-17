import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import struct
#import statistics as st

#records = 0
#medias = []
#deltas = []
fc = 1420.0
bw = 100.0
freq = np.linspace(fc - bw/2.0, fc + bw/2.0, num=2048)

def raw2df(raw):
    '''
    Funcion para convertir datos RAW a DataFrame
    '''
    spch = 2048
    bspl = 8
    size = os.path.getsize(raw.name)
    nrec = int(size/spch/bspl)
    dt = np.dtype('q')
    dt = dt.newbyteorder('>')
    data = raw.read()
    np_data = np.frombuffer(data, dt)
    np_data.resize(nrec,spch)
    np_data = np.transpose(np_data)
    df = pd.DataFrame(np_data)
    return df

def spprom(raw):
    '''
    Promedia los espectros del DataFrame y grafica
    '''
    spprom = raw.mean(axis=1)
    plt.plot(freq,spprom)
    plt.yscale('log')
    plt.title('Espectro promediado de todo el archivo')
    plt.xlabel('Frecuencia [MHz]')
    plt.ylabel('Amplitud [cuentas]')
    plt.show()

def read_mdata(mdata):
    '''
    Leer archivos metadata con datos de la observacion
    Datos a extraer:
    nombre de la fuente, RA, DEC, Fecha obs, Hora obs UTC
    '''
    pass

def df2fb(dframe):
    '''
    Convertir DataFrame a Filterbank
    '''
    pass

def invrawch(raw):
    '''
    Invierte orden de canales para formato FB
    '''
    spch = 2048
    bspl = 8
    size = os.path.getsize(raw.name)
    nrec = int(size/spch/bspl)
    gf = open('test.dat','wb')
    for rec in range(0,nrec):
        spraw = raw.read(spch*bspl)
        splis = struct.unpack_from(">2048q",spraw)
        splis = list(splis)
        splis.reverse()
        splis = tuple(splis)
        spinv = struct.pack(">2048q",*splis)
        gf.write(spinv)
    return 


if __name__ == "__main__":
    fd = open("../raw_data/20201027_133329_test.raw", "rb")
#    fd1 = open("./test.dat", "rb")
#    invrawch(fd)
    data = raw2df(fd)
    print(data[0])
#    data2  = raw2df(fd1)
#    print(data2[3])
#    spprom(data2)
    fd.close()
#    fd1.close()
#    spprom = data.mean(axis=1)
#    print(len(spprom))
#    print(spprom[0])
#    plt.plot(spprom)
#    plt.yscale('log')
#    plt.show()


#with open("../../dirtest/20201027_133329_0.raw", "rb") as fd:
#with open("../raw_data/20201027_133329_1m.raw", "rb") as fd:
#    fecha, hora, resto = fd.name.split('_')
#    print(fecha, hora)
#    dt = np.dtype('q')
#    dt = dt.newbyteorder('>')
#    data = fd.read()
#    np_data = np.frombuffer(data, dt)
##    np_data.resize(720, 2048)
#    np_data.resize(24358,2048)
#    np_data = np.transpose(np_data)
#    df = pd.DataFrame(np_data)
#    for j in range(0,720):
#        medias.append(df[j].mean())
#        deltas.append(np.abs(df[j].mean() - 16288))
#
#plt.hist(medias, bins=20)
#plt.show()
#plt.hist(deltas, bins=20)
#plt.show()
#print(st.mean(medias), st.stdev(medias))
#print("End")
