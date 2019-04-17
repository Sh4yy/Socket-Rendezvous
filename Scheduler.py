## this is the main scheduler class
## scheduler takes care of expirations and users
from time import time, sleep
import functools
from sortedcollections import SortedList
from threading import Thread
from enum import Enum

@functools.total_ordering
class ScheduleItem:

    def __init__(self, client_id, expiration):
        self.client_id = client_id
        self.exp = expiration

    def set_exp(self, ttl):
        """
        update the item's expiration time from now
        :param ttl: seconds from now
        """
        self.exp = time() + ttl

    def is_expired(self):
        return time() > self.exp

    def __lt__ (self, other):
        return self.exp < other.exp

    def __eq__ (self, other):
        return self.exp == other.exp

class Scheduler:

    def __init__(self, pending_time):
        """ initialize a new Scheduler """
        self.item_map = dict() # map for fast lookup
        self.online_list = SortedList()
        self.pending_list = SortedList()
        self.pending_time = pending_time

    def start_running(self):

        def processor():
            while True:
                sleep(1)
                self._check_online_list()
                self._check_pending_list()

        thread = Thread(target=processor)
        thread.start()

    def _check_online_list(self):

        for item in self.online_list:
            if not item.is_expired():
                break

            self.online_list.remove(item)
            item.set_exp(self.pending_time)
            self.pending_list.add(item)

    def _check_pending_list(self):

        for item in self.pending_list:
            if not item.is_expired():
                break

            self.pending_list.remove(item)
            del self.item_map[item.client_id]

    def add(self, item):
        self.online_list.add(item)
        self.item_map[item.client_id] = item

    def expire(self, key, ttl):
        status = self.status(key)
        if status == Status.Online:
            self.item_map[key].set_exp(ttl)
            return True

        elif status == Status.Pending:
            raise NeedsVerification()

        elif sattus == Status.DNE:
            raise DoesNotExist()

    def delete(self, key):
        status = self.status(key)
        if status == Status.Online:
            self.online_list.remove(key)
            del self.item_map[key]
            return True
        elif status == Status.Pending:
            self.pending_list.remove(key)
            del self.item_map[key]
            return True
        else:
            return False

    def verify(self, key, tts):
        status = self.status(key)
        if status == Status.Pending:
            self.pending_list.remove(key)
            item = item_map[key]
            item.set_exp(tts)
            self.online_list.add(item)
            return True
        elif status == Status.DNE:
            raise DoesNotExist()
        else:
            return False

    def status(self, key):
        if key in self.item_map:
            item = self.item_map[key]
            if item in self.online_list:
                return Status.Online
            elif item in self.pending_list:
                return Status.Pending
            else:
                raise Exception('something went wrong')
        else:
            return Status.DNE

class Status(Enum):
    Online = 'Online'
    Pending = 'Pending'
    DNE = 'DoesNotExist'

class NeedsVerification(Exception):
    pass

class DoesNotExist(Exception):
    pass


if __name__ == '__main__':
    s = Scheduler(3 * 10)
    item = ScheduleItem("hey", 5)
    s.add(item)

    print(s.item_map)
    print(s.online_list)
    print(s.pending_list)

    s.start_running()
    while True:
        print(s.item_map)
        print(s.online_list)
        print(s.pending_list)
        sleep(1)
