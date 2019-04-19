from time import time, sleep
import functools
from sortedcollections import SortedList
from threading import Thread, Lock
from enum import Enum


class Status(Enum):
    Online = 'Online'
    Pending = 'Pending'
    DNE = 'DoesNotExist'


@functools.total_ordering
class ScheduleItem:

    def __init__(self, client_id, status=Status.Online, ttl=None):
        self.client_id = client_id
        self.status = status
        self.exp = None
        self.lock = Lock
        if ttl:
            self.set_exp(ttl)

    def set_exp(self, ttl):
        """
        update the item's expiration time from now
        :param ttl: seconds from now
        """
        self.exp = time() + ttl

    def is_expired(self):
        return time() > self.exp

    def __lt__(self, other):
        return self.exp < other.exp

    def __eq__(self, other):
        return self.exp == other.exp

    def __repr__(self):
        template = "ScheduleItem(client_id={}, exp={}, status={})"
        return template.format(self.client_id, self.exp - time(), self.status.value)


class Scheduler:

    def __init__(self, error_time):
        """ initialize a new Scheduler """
        self.item_map = dict()
        self.item_list = SortedList()
        self.error_time = error_time
        self.lock = Lock()

    def start_running(self):

        def processor():
            while True:
                sleep(1)
                self._process_list()

        thread = Thread(target=processor)
        thread.start()

    def _process_list(self):

        for item in self.item_list:
            if not item.is_expired():
                break

            self._process_item(item)

    def _process_item(self, item):

        with self.lock:
            self.item_list.remove(item)
            if item.status == Status.Online:
                item.set_exp(self.error_time)
                item.status = Status.Pending
                self.item_list.add(item)

            elif item.status == Status.Pending:
                del self.item_map[item.client_id]

    def add(self, item):
        with self.lock:
            self.item_list.add(item)
            self.item_map[item.client_id] = item

    def get(self, key):
        if key in self.item_map:
            return self.item_map[key]

        return None

    def expire(self, key, ttl):
        status = self.status(key)
        if status == Status.Pending:
            raise NeedsVerification()
        elif status == Status.DNE:
            raise DoesNotExist()
        with self.lock:
            item = self.item_map(key)
            self.item_list.remove(item)
            item.set_exp(ttl)
            self.item_list.add(item)
            return True

    def delete(self, key):
        status = self.status(key)
        if status == Status.DNE:
            return False
        with self.lock:
            item = self.item_map[key]
            self.item_list.remove(item)
            del self.item_map[key]
            return True

    def verify(self, key, ttl):
        status = self.status(key)
        if status == Status.DNE:
            raise DoesNotExist()
        elif status == Status.Online:
            return False
        with self.lock:
            item = self.item_map[key]
            item.set_exp(ttl)
            item.status = Status.Online
            return True

    def status(self, key):
        if key in self.item_map:
            item = self.item_map[key]
            return item.status
        else:
            return Status.DNE


class NeedsVerification(Exception):
    pass


class DoesNotExist(Exception):
    pass
