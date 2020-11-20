import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statistics as st

records = 0
medias = []
deltas = []

fd = open("../../dirtest/20201027_133329_0.raw", "rb") 
spch = 2048
size = os.path.getsize(fd.name)
print(spch,size/8/spch,size)


