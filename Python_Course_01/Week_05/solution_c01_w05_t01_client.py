import socket
import time


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection((self.host, self.port), 5)
        self.sock.settimeout(self.timeout)

    def put(self, metric, val, timestamp=None):
        timestamp = timestamp or int(time.time())
        if isinstance(val, str):
            try:
                val = int(val)
            except ValueError:
                val = float(val)
        metric, timestamp = str(metric).strip(), int(timestamp)
        command = f"put {metric} {val} {timestamp}\n"
        try:
            # print(f'client will try to send {command.encode("utf8")}')
            self.sock.sendall(command.encode("utf8"))
            response = self.sock.recv(1024)
            response = response.decode("utf-8")
            print(f'client recieved the response:\n{response}')
            if "ok\n" not in response:
                raise ClientError
        except socket.error:
            raise ClientError

    def get(self, metric) -> dict:
        metric = str(metric).strip()
        command = f"get {metric}\n"
        try:
            # print(f'client will try to send {command.encode("utf8")}')
            self.sock.sendall(command.encode("utf8"))
            response = self.sock.recv(1024)
            response = response.decode("utf-8")
            # print(f'client recieved the response:\n{response}')
            if "ok\n" not in response:
                raise ClientError
            else:
                response_dict = self.parse(response)
        except:
            raise ClientError
        return response_dict

    @staticmethod
    def parse(response) -> dict:
        response_dict = {}
        response_list = response.split("\n")
        for i in range(1, len(response_list) - 2):
            params = response_list[i].split()
            metric, val, timestamp = params[0], float(params[1]), int(params[2])
            response_dict[metric] = response_dict.get(metric, []) + [(timestamp, val)]
        for k, v in response_dict.items():
            v.sort(key=lambda x: x[0])
        return response_dict
