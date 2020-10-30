# deepspyce.py

# https://blimpy.readthedocs.io


# 
- deepspyce/
    - __init__.py
    - dom.py/core.py/base.py
    - io/
        - __init__.py
        - raw_io.py
        - common_io.py
    - proccess.py
    - datasets
        - __init__.py
        - archivo1.fits
        - archivo2.fits




from astropy.table import Table

import blimpy


class Spectrum(...):
    ...




def read_fits(path)
    dat = Table.read(path, format='fits')
    df = dat.to_pandas()
    
    # posprocesarlo
    
    return Spectrun(dfp)
    
    
def read_filterbank(path):
    ....


#===============================================================================
# USER
#===============================================================================
import deepspyce as dspy


espect = dspy.read_fits()

espect = dspy.read_filterbank()
