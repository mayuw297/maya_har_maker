import scapy
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sniff

FACEBOOK_IP = "157.240.20.35"
packs = []
def filterFcebook(pack):
    return IP in pack and (pack[IP].src==FACEBOOK_IP or pack[IP].dst==FACEBOOK_IP)

def sniffPacks():
    global packs
    packs = sniff( lfilter=filterFcebook,count = 20)


def write():
    pass
def main():
    global packs

    sniffPacks()
    for p in packs:
        if scapy.packet.Raw in p:
            print (p[scapy.packet.Raw])
        print(p[TCP].seq,p[TCP].ack)

if __name__ =="__main__":
    main()