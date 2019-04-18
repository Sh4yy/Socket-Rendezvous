from .Scheduler import ScheduleItem, Scheduler
from .Config import config
from .Random import PeerID
from expiringdict import ExpiringDict


class Client(ScheduleItem):

    def __init__(self, *args, **kwargs):
        peer = PeerID()
        super(ScheduleItem).__init__(client_id.peer.id_hex, *args, **kwargs)
        self.private_id = private_id
        self.peer = peer
        self.host = None
        self.port = None

    def set_address(self, host, port):
        self.host = host
        self.port = port

    def get_address(self):
        return (self.host, self.port)


scheduler = Scheduler(config['error_time'])
reg_cache = ExpiringDict(max_len=100, max_age_seconds=60)
