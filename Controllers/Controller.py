from Models import Client
from Utilities.Scheduler import Scheduler, NeedsVerification, DoesNotExist
from Utilities.Config import config
from datetime import timedelta
from time import time
from Utilities.HBExceptions import *


class Controller:

    _key_private = {}
    _scheduler = Scheduler(config['error_time'])

    @classmethod
    def start_scheduler(cls):
        """ start scheduler """
        cls._scheduler.start_running()

    @classmethod
    def register(cls):
        """
        register a new client
        :return: Client instance
        """

        client = Client()
        client.set_exp(timedelta(minutes=5).seconds)
        cls._scheduler.add(client)
        return client

    @classmethod
    def verify(cls, client_id, private_id):
        """
        verify a user after not having activity
        :param client_id: user's client id
        :param private_id: user's private id
        :return: True on success
        """

        return cls._scheduler.verify(client_id, ttl=30)

    @classmethod
    def logout(cls, client_id, private_id):
        """
        logout a user from the server
        :param client_id: user's client id
        :param private_id: user's private id
        :return: True on success
        """

        if private_id in cls._key_private:
            del cls._key_private[private_id]

        cls._scheduler.delete(client_id)
        return True

    @classmethod
    def get_client(cls, client_id):
        """
        get client
        :param client_id: target's client_id
        :return: client instance
        """

        return cls._scheduler.get(client_id)

    @classmethod
    def get_private_to_id(cls, private_key):
        """
        get client id from private key
        :param private_key: target private key
        :return: client id if exists
        """

        if private_key in cls._key_private:
            return cls._key_private[private_key]

        return None

    @classmethod
    def heartbeat(cls, private_key, host, port):
        """
        record a new heartbeat
        :param private_key: client's private key
        :param host: client's host string
        :param port: client's port
        :return: True on success
        """

        if not private_key in cls._key_private:
            raise HBDoesNotExist()

        client_id = cls.get_private_to_id(private_key)
        client = cls.get_client(client_id)
        client.set_address(host, port)
        client.last_pulse = time()

        try:
            cls._scheduler.expire(client_id, ttl=30)
        except NeedsVerification:
            raise HBNeedsVerification()
        except DoesNotExist:
            raise HBDoesNotExist()

        return True
