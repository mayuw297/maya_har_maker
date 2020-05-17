import _thread
import scapy
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sniff
import datetime
import time
import json
import re

MOMO_IP = "158.106.133.146"


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# key is request ack. values request seq and responses seqs.
client_requests = {}
latest_server_ack = -1
latest_server_seq = -1

REQUEST_DATA = 4
RESPONSES_DATA = 3
TOTAL_LENGTH = 2
LATEST_TIME = 1
FIRST_TIME = 0


def request_type_indicator(request):
    pattern = "(?<=GET )(.*)(?= HTTP)"
    substring = re.search(pattern, request).group(1)
    splits = substring.split(".")
    type = splits[-1]
    return type

    pass
def write_data_to_json_file(file_path):
    global client_requests

    data = {}


    for key in client_requests:
        request_sequence = client_requests[key][1]
        data[request_sequence] = {}
        total_responses_length = client_requests[key][0][TOTAL_LENGTH]
        #making sure we only collect non empty sessions
        if total_responses_length==0:
            continue
        late = client_requests[key][0][LATEST_TIME]
        first = client_requests[key][0][FIRST_TIME]
        diff = (late-first)
        responses_array = client_requests[key][0][RESPONSES_DATA]
        request_type = request_type_indicator(str(client_requests[key][0][REQUEST_DATA]))
        data[request_sequence]["total_responses_length"] = total_responses_length
        data[request_sequence]["total_time"] = diff.total_seconds()
        data[request_sequence]["request_type"] = request_type
       # data[request_sequence]["responses_array"] = responses_array

    #clear prev content
    open(file_path, 'w').close()
    # dump json
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile)
def filterSite(pack):

    is_it = False
    if IP in pack and TCP in pack and scapy.packet.Raw in pack and (pack[IP].dst == MOMO_IP or pack[IP].src == MOMO_IP):
        is_it = True
        inspect_single_pack(pack)
    return  is_it


def inspect_single_pack(pack):
    global latest_server_ack
    global latest_server_seq
    global client_requests
    print("------------------------------------")

    print("ACK: " + bcolors.OKGREEN + str(pack[TCP].ack) + str(pack[scapy.packet.Raw]) + bcolors.ENDC)
    print("SEQ: " + bcolors.WARNING + str(pack[TCP].seq) + str(pack[scapy.packet.Raw]) + bcolors.ENDC)

    if pack[IP].dst == MOMO_IP:
        print(bcolors.FAIL + "CLIENT" + bcolors.ENDC)
        # a new request.
        client_requests[pack[TCP].ack] = [[0, 0, 0, [], 0], pack[TCP].seq]
        client_requests[pack[TCP].ack][0][FIRST_TIME] = datetime.datetime.now()
        client_requests[pack[TCP].ack][0][REQUEST_DATA] = pack[scapy.packet.Raw]
    if pack[IP].src == MOMO_IP:
        print(bcolors.FAIL + "SERVER" + bcolors.ENDC)

        # continuous acks
        if pack[IP].ack == latest_server_ack:
            client_requests[latest_server_seq].append(pack[TCP].seq)
            ##updating data
            client_requests[latest_server_seq][0][LATEST_TIME] = datetime.datetime.now()
            client_requests[latest_server_seq][0][TOTAL_LENGTH] += len(pack[scapy.packet.Raw])
            client_requests[latest_server_seq][0][RESPONSES_DATA].append(str(pack[scapy.packet.Raw]))
            ##
        elif pack[TCP].seq in client_requests:
            client_requests[pack[TCP].seq].append(pack[TCP].seq)
            ## updating data
            client_requests[pack[TCP].seq][0][LATEST_TIME] = datetime.datetime.now()
            client_requests[pack[TCP].seq][0][TOTAL_LENGTH] += len(pack[scapy.packet.Raw])
            client_requests[pack[TCP].seq][0][RESPONSES_DATA].append(str(pack[scapy.packet.Raw]))

            ##
            latest_server_ack = pack[TCP].ack
            latest_server_seq = pack[TCP].seq

    print("------------------------------------")

def main():
    #sniff packs
    packs = sniff(lfilter=filterSite, count=1000)
    # writing to json file
    write_data_to_json_file("final.txt")


if __name__ =="__main__":
    main()