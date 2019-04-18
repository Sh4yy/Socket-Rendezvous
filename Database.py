from Scheduler import ScheduleItem, Scheduler
from Config import config

class Client(ScheduleItem):

    def __init__(self, client_id, private_id, host, port, *args, **kwargs):
        super(ScheduleItem).__init__(client_id=client_id, *args, **kwargs)
        self.private_id = private_id
        self.host = host
        self.port = port

scheduler = Scheduler(config['error_time'])
