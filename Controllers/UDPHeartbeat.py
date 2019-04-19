import socket
from .Controller import Controller
from threading import Thread
from Utilities.HBExceptions import *


class UDPHeartbeat:

    def __init__(self, host, port):
        """
        initialize the heartbeat instance
        :param host: heartbeat host
        :param port: heartbeat port
        """
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((host, port))
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _process_socket(self):
        """ processes the socket input data """

        success_code = struct.pack('!i', 1020)
        while True:
            pk_bytes, addr = self._sock.recvfrom(32)
            private_key = pk_bytes.decode()

            try:
                Controller.heartbeat(private_key, addr[0], addr[1])
                self._sock.sendto(success_code, addr)
            except HBException as e:
                self._sock.sendto(e.code_bytes, addr)

    def start_running(self):
        """ starts a new thread for socket heartbeat """
        thread = Thread(target=self._process_socket)
        thread.start()
        return True
