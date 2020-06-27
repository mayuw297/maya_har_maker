import scapy
from scapy.layers.inet import TCP, IP

from constants import MOMO_IP, BColors
from packetHandler import ResponseHandler, RequestHandler


class Filter:
    @staticmethod
    def filter_site(pack) -> bool:
        if IP in pack and \
                TCP in pack and \
                scapy.packet.Raw in pack and \
                (pack[IP].dst == MOMO_IP or pack[IP].src == MOMO_IP):
            Filter.inspect_single_pack(pack)

            return True

        return False

    @classmethod
    def inspect_single_pack(cls, pack):
        Filter.print_progress(pack)

        if pack[IP].dst == MOMO_IP:
            RequestHandler.handle_packet(pack)
        else:
            ResponseHandler.handle_packet(pack)

    @staticmethod
    def print_progress(pack):
        print("------------------------------------")
        print("ACK: " + BColors.OKGREEN + str(pack[TCP].ack) + str(pack[scapy.packet.Raw]) + BColors.ENDC)
        print("SEQ: " + BColors.WARNING + str(pack[TCP].seq) + str(pack[scapy.packet.Raw]) + BColors.ENDC)
