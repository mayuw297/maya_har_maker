from datetime import datetime


class ClientsRequests:
    def __init__(self):
        self._data = {}

    def __getitem__(self, item: int) -> 'Data':
        return self._data[item]

    def __contains__(self, item: int) -> bool:
        return True if item in self._data else False

    def add(self, item: int):
        self._data[item] = self.Data()

    class Data:
        def __init__(self):
            self.request_data = []
            self.response_data = []
            self.total_length = 0
            self.latest_time: datetime
            self.first_time: datetime

        def __dict__(self):
            return {'request_data': self.request_data.__str__(),
                    'response_data': ''.join(self.response_data),
                    'total_length': self.total_length,
                    'latest_time': self.latest_time.strftime('%H:%M:%S'),
                    'first_time': self.first_time.strftime('%H:%M:%S')}
