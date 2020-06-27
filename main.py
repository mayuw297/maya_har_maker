from scapy.all import *

import constants
import filter


def main():
    # Clear previous content
    open(constants.LOG_FILE, 'w').close()

    # Sniff packets
    sniff(lfilter=filter.Filter.filter_site)


if __name__ == "__main__":
    main()
