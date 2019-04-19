from Utilities.Scheduler import ScheduleItem
import os


class PeerID:

    def __init__(self, id_len=16, key_len=32):
        self._id = os.urandom(id_len)
        self._key = os.urandom(key_len)

    @property
    def id_bytes(self):
        return self._id

    @property
    def id_hex(self):
        return self._id.hex()

    @property
    def key_bytes(self):
        return self._key

    @property
    def key_hex(self):
        return self._key.hex()


class Client(ScheduleItem):

    def __init__(self):
        peer = PeerID()
        super().__init__(peer.id_hex)
        self.private_id = peer.key_hex
        self.peer = peer
        self.host = None
        self.port = None
        self.last_pulse = 0

    def set_address(self, host, port):
        self.host = host
        self.port = port

    def get_address(self):
        return self.host, self.port


