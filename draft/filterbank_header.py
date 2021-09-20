from datetime import datetime
import struct
import sys,argparse
from astropy.time import Time
#import thread
import time
import os


def build_file(args): 

	with open(args.iar_file+".iar", "r") as ins:
		array = []
		for line in ins:
			array.append(line.split(","))

	#Valor de la ROACH
	fft_pts=128
	adc_clk=200e6
	#-
	source_name=array[0][1].rstrip()
	source_ra=float(array[1][1])
	source_dec=float(array[2][1])
	ref_dm=float(array[3][1])
	pul_period=float(array[4][1])
	high_freq=float(array[5][1])
	telescope_id=int(array[6][1])
	machine_id=int(array[7][1])
	data_type=int(array[8][1])
	observing_time=float(array[9][1])
	local_oscilator=float(array[10][1])
	gain=int(array[11][1])
	bandwidth=int(array[12][1])
	avg_data=int(array[13][1])
	sub_bands=int(array[14][1])

	secs=int(datetime.now().strftime('%S'))+2
	file_time=datetime.now().strftime('_%Y%m%d_%H%M'+str(secs)+'.fil')
	times = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:'+str(secs))
	t_start = (Time(times, format='isot', scale='utc')).mjd
	out_file="ds"+str(avg_data)+"_"+source_name+file_time
	#con parametros de la ROACH
	tsamp=float((avg_data*fft_pts)/adc_clk)
	f_off=(float(adc_clk/2)/float(fft_pts/2))/1e6

	print ("Source Name: "+source_name)
	print ("Period: " + str(pul_period))
	print ("DM: " + str(ref_dm))
	print ("Highest Freq[MHz]: " + str(high_freq))
	print ("Observing Time[min]: " + str(observing_time))
	print ("Total Band Width[MHz]: " + str(bandwidth))
	print ("Average value: " + str(avg_data))
	print ("Number of channels: " + str(sub_bands))
	print ("Samplig Time[uS]: " + str(tsamp/1e-6))
	print ("Channel BW[MHz]: " + str(f_off))

	#tsamp=((1/(float(bandwidth)*1e6)))*avg_data
	fp = open(out_file, "wb")


	stx="HEADER_START"
	etx="HEADER_END"
	fp.write(struct.pack('i', len(stx))+stx.encode())
	fp.flush()
	#--
	aux="rawdatafile"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	fp.write(struct.pack('i', len(out_file))+out_file.encode())
	#--
	aux="src_raj"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('d', source_ra)
	fp.write(aux)
	fp.flush()


	#--
	aux="src_dej"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('d', source_dec)
	fp.write(aux)
	#--
	aux="az_start"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('d', 0.0)
	fp.write(aux)
	#--
	aux="za_start"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('d', 0.0)
	fp.write(aux)
	#--
	aux="tstart"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('d', float(t_start))
	fp.write(aux)
	#--
	aux="foff"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('d', f_off)
	fp.write(aux)
	#--
	aux="fch1"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('d', high_freq)
	fp.write(aux)
	#--
	aux="nchans"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('i', sub_bands)
	fp.write(aux)
	#--
	aux="data_type"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('i', 1)
	fp.write(aux)
	#--
	aux="ibeam"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('i', 1)
	fp.write(aux)
	#--
	aux="nbits"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('i', 32)
	fp.write(aux)
	#--
	aux="tsamp"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('d', tsamp)
	fp.write(aux)
	#--
	aux="nbeams"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('i', 1)
	fp.write(aux)
	#--
	aux="nifs"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('i', 1)
	fp.write(aux)
	#--
	aux="source_name"
	fp.write(struct.pack('i', len(aux))+aux.encode())
	fp.write(struct.pack('i', len(source_name))+source_name.encode())
	#--
	aux="machine_id"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('i', machine_id)
	fp.write(aux)
	#--
	aux="telescope_id"
	aux=struct.pack('i', len(aux))+aux.encode()
	fp.write(aux)
	aux=struct.pack('i', telescope_id)
	fp.write(aux)
	#--
	fp.write(struct.pack('i', len(etx))+etx.encode())
	fp.flush()
	fp.close
	return [out_file,high_freq, bandwidth, gain, avg_data, sub_bands,observing_time,tsamp]
