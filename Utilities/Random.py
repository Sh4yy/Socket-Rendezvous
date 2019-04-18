import os

class PeerID:

    def __init__(self, id_len=16, key_len=64):
        self._id = os.urandom(id_len)
        slef._key = os.urandom(key_len)

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
