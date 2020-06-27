import datetime

import scapy
from scapy.layers.inet import TCP

import clientsRequests
import constants
import log


class PacketHandler:
    client_requests = clientsRequests.ClientsRequests()

    # key is request ack. values request seq and responses seqs.
    latest_server_ack = -1
    latest_server_seq = -1

    @classmethod
    def handle_packet(cls, pack):
        """Handle the packet with respect to it being a client request
        or a server response."""
        pass

    @classmethod
    def update_data(cls, pack, x):
        cls.client_requests[x].latest_time = datetime.datetime.now()
        cls.client_requests[x].total_length += len(pack[scapy.packet.Raw])
        cls.client_requests[x].response_data.append(str(pack[scapy.packet.Raw]))


class RequestHandler(PacketHandler):
    @classmethod
    def handle_packet(cls, pack):
        """Handle a client request packet"""

        ack = pack[TCP].ack

        print(constants.BColors.FAIL + "CLIENT" + constants.BColors.ENDC)

        if ack not in cls.client_requests:
            cls.client_requests.add(ack)

        cls.client_requests[ack].first_time = datetime.datetime.now()
        cls.client_requests[ack].request_data = pack[scapy.packet.Raw]

        print("------------------------------------")


class ResponseHandler(PacketHandler):
    @classmethod
    def handle_packet(cls, pack):
        """Handle a server response"""

        ack = pack[TCP].ack
        seq = pack[TCP].seq

        print(constants.BColors.FAIL + "SERVER" + constants.BColors.ENDC)

        # Continue acks handling.
        if ack == cls.latest_server_ack:
            cls.update_data(pack, cls.latest_server_seq)
        elif seq in cls.client_requests:
            # Update whole last session to file.
            log.Log.write_session_data_to_json_file(cls.latest_server_seq)
            cls.update_data(pack, seq)

            ##
            cls.latest_server_ack = ack
            cls.latest_server_seq = seq

            print("------------------------------------")
