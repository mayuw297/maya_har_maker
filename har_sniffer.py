import _thread
import scapy
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sniff

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
def filterSite(pack):
    global latest_server_ack
    global latest_server_seq
    is_it = False
    if scapy.packet.Raw in pack:
        #print("LEN: "+bcolors.OKBLUE+str(len(pack[scapy.packet.Raw]))+bcolors.ENDC)

        if IP in pack and pack[IP].dst == MOMO_IP:
            is_it = True
            # a new request.
            client_requests[pack[TCP].ack]  = [pack[TCP].seq]


            #print("ACK: "+bcolors.OKGREEN + str(pack[TCP].ack) + bcolors.ENDC)

            #print("SEQ: "+str(pack[TCP].seq), pack[scapy.packet.Raw])
        if IP in pack and pack[IP].src == MOMO_IP:
            is_it=True
            # if current server request is the a continuos request of a prev server request, keep it's sequence num back together
            if pack[TCP].ack == latest_server_ack:
                client_requests[latest_server_seq].append(pack[TCP].seq)
            else:
                # if current server request isnt a continous one, keep it alone, update the new 'latest server' vars
                client_requests[pack[TCP].seq].append(pack[TCP].seq)
                latest_server_ack = pack[TCP].ack
                latest_server_seq = pack[TCP].seq

            #print("ACK: "+bcolors.OKGREEN + str(pack[TCP].ack) + bcolors.ENDC)
            #print("SEQ: "+bcolors.WARNING + str(pack[TCP].seq)+str(pack[scapy.packet.Raw])+ bcolors.ENDC)
    return  is_it

def main():
    packs = sniff(lfilter=filterSite, count=1000)
    print (client_requests)



if __name__ =="__main__":
    main()