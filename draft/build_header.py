# Acknowledgements to Guillermo Gancio

# from argparse import ArgumentParser
from datetime import datetime

from filterbank_header import build_file


def main():
    # parser = ArgumentParser(description="Pulsar adquisition programm")
    # parser.add_argument(
    #     "-p", "--iar-file",
    #     dest="path", type=str,
    #     help="IAR file name",
    #     required=True
    # )
    # args = parser.parse_args()

    path = input("Please, enter your .iar data path: ")

    print(datetime.now().strftime("Current Time: %Y%m%d %H%M%S"))
    [
        out_file,
        high_freq,
        bandwidth,
        gain,
        avg_data,
        sub_bands,
        observing_time,
        tsamp,
    ] = build_file(path)

    print(out_file)


if __name__ == "__main__":
    main()
