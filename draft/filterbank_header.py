import io
import struct
from datetime import datetime

from astropy.time import Time


def writer(
    file: io.BufferedReader,
    name=None,
    value=None,
    name_fmt="<i",
    value_fmt="<d",
):
    if isinstance(name, str):
        file.write(struct.pack(name_fmt, len(name)) + name.encode())
    if value is not None:
        file.write(struct.pack(value_fmt, value))

    return


def build_file(path: str) -> list:

    with open(path, "r") as f:
        data = [line.split(",") for line in f]

    # Valor de la ROACH
    fft_pts = 128
    adc_clk = 200e6
    # -
    source_name = data[0][1].strip()
    source_ra = float(data[1][1])
    source_dec = float(data[2][1])
    ref_dm = float(data[3][1])
    pul_period = float(data[4][1])
    high_freq = float(data[5][1])
    telescope_id = int(data[6][1])
    machine_id = int(data[7][1])
    # data_type = int(data[8][1])
    observing_time = float(data[9][1])
    # local_oscilator = float(data[10][1])
    gain = int(data[11][1])
    bandwidth = int(data[12][1])
    avg_data = int(data[13][1])
    sub_bands = int(data[14][1])

    utc_now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    time_now = datetime.now().strftime("_%Y%m%d_%H%M%S.fil")
    # Modified Julian Date
    mjd_now = float(Time(utc_now, format="isot", scale="utc").mjd)
    out_file = "ds" + str(avg_data) + "_" + source_name + time_now
    # con parametros de la ROACH
    tsamp = float((avg_data * fft_pts) / adc_clk)
    f_off = (float(adc_clk / 2) / float(fft_pts / 2)) / 1e6

    print("Source Name: " + source_name)
    print("Period: " + str(pul_period))
    print("DM: " + str(ref_dm))
    print("Highest Freq[MHz]: " + str(high_freq))
    print("Observing Time[min]: " + str(observing_time))
    print("Total Band Width[MHz]: " + str(bandwidth))
    print("Average value: " + str(avg_data))
    print("Number of channels: " + str(sub_bands))
    print("Samplig Time[uS]: " + str(tsamp / 1e-6))
    print("Channel BW[MHz]: " + str(f_off))

    # tsamp=((1/(float(bandwidth)*1e6)))*avg_data
    with open(out_file, "wb") as o_f:

        writer(o_f, "HEADER_START")
        writer(o_f, "rawdatafile")
        writer(o_f, out_file)
        writer(o_f, "src_raj", source_ra)
        writer(o_f, "src_dej", source_dec)
        writer(o_f, "az_start", 0.0)
        writer(o_f, "za_start", 0.0)
        writer(o_f, "tstart", mjd_now)
        writer(o_f, "foff", f_off)
        writer(o_f, "fch1", high_freq)
        writer(o_f, "nchans", sub_bands)
        writer(o_f, "data_type", 1, value_fmt="i")
        writer(o_f, "ibeam", 1, value_fmt="i")
        writer(o_f, "nbits", 32, value_fmt="i")
        writer(o_f, "tsamp", tsamp)
        writer(o_f, "nbeams", 1, value_fmt="i")
        writer(o_f, "nifs", 1, value_fmt="i")
        writer(o_f, "source_name")
        writer(o_f, source_name)
        writer(o_f, "machine_id", machine_id, value_fmt="i")
        writer(o_f, "telescope_id", telescope_id, value_fmt="i")
        writer(o_f, "HEADER_END")

    return [
        out_file,
        high_freq,
        bandwidth,
        gain,
        avg_data,
        sub_bands,
        observing_time,
        tsamp,
    ]
