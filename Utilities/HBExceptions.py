import struct


class HBException(Exception):

    code = 0000
    reason = "default exception".title()

    @property
    def code_bytes(self):
        return struct.pack('!i', self.code)


class HBDoesNotExist(HBException):

    code = 1060
    reason = "client was not found".title()


class HBNeedsVerification(HBException):

    code = 1050
    reason = "must re-verify you're address".title()

