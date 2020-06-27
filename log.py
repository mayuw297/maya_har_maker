import json
import re
from json import JSONEncoder

import constants
import packetHandler


class Log:
    @classmethod
    def write_session_data_to_json_file(cls, latest_server_seq):
        client_requests = packetHandler.PacketHandler.client_requests

        if latest_server_seq == -1:
            print("No response yet.")
            return

        request_sequence = client_requests[latest_server_seq]

        # Making sure we only collect non empty sessions
        if request_sequence.total_length == 0:
            return

        # dump json
        with open(constants.LOG_FILE, 'a') as outfile:
            json.dump(request_sequence.__dict__(), outfile)

            outfile.write("\n\n")
            outfile.write("total data: ")
            outfile.write(request_sequence.__dict__().__str__())
            outfile.write("\n********************\n")

    @classmethod
    def request_type_indicator(cls, request):
        pattern = "(?<=GET )(.*)(?= HTTP)"
        substring = re.search(pattern, request).group(1)
        splits = substring.split(".")
        type = splits[-1]

        return type
