#acknowledgement to Guillermo Gancio

from filterbank_header import *
import time
import os
from datetime import datetime
import struct
import sys,argparse



def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    return parser

def main():
        parser = argparse.ArgumentParser(description='Pulsar adquisition programm')
        parser.add_argument('-p','--iar-file', help='IAR file name',required=True)
        args = parser.parse_args()

        print(datetime.now().strftime('Current Time: %Y%m%d %H%M%S'))
        [out_file,high_freq, bandwidth, gain, avg_data, sub_bands,observing_time,tsamp] = build_file(args)

        print(out_file)

if __name__ == '__main__':
    main()

