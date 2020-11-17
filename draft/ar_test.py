import numpy as np

fd = open('testdf.csv','r')
gd = open('testdf.txt','w')

datos = fd.readlines()

print('([ ')
for i in range(0,2048):
    data = datos[i].split(',')
    s = '[' + str(data[0]) + ',' + str(data[1]).rstrip('\n') + '],'
    print(s)
print('])')

