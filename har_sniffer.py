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
packs = []
def filterSite(pack):
    global packs
    if scapy.packet.Raw in pack:
        print("LEN: "+bcolors.OKBLUE+str(len(pack[scapy.packet.Raw]))+bcolors.ENDC)

        if IP in pack and pack[IP].dst == MOMO_IP:
            print("ACK: "+bcolors.OKGREEN + str(pack[TCP].ack) + bcolors.ENDC)
            packs+=pack
            print("SEQ: "+str(pack[TCP].seq), pack[scapy.packet.Raw])
        if IP in pack and pack[IP].src == MOMO_IP:
            print("ACK: "+bcolors.OKGREEN + str(pack[TCP].ack) + bcolors.ENDC)
            print("SEQ: "+bcolors.WARNING + str(pack[TCP].seq)+str(pack[scapy.packet.Raw])+ bcolors.ENDC)
def sniffPacks():
    sniff( lfilter=filterSite)

def sortAcks():
    global packs
def main():
    global packs
    sniffPacks()



if __name__ =="__main__":
    main()