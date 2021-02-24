from .constants import *
from .common_packet import CommonPacket


def _create_payload(type_id: int, service_id: int, cmd_id: int, cmd_value: int):
    if type_id is None:
        raise Exception('No SA Type ID assigned. Execute [register] first.')

    _payload = [6,
                type_id,
                (cmd_id << 7) | service_id,
                ] + list(cmd_value.to_bytes(2, 'big')) + [0]
    for x in _payload[:-1]:
        _payload[-1] ^= x
    return _payload


def _parse_payload(payload: list):
    raise NotImplementedError


class SmartApplication:

    def __init__(self, port='/dev/ttyUSB0'):
        """"""
        self.port = port
        self._sa_type = None

    def request(self, payload):
        """Send a Packet request for SA."""
        raise NotImplementedError

    def register(self):
        """Send a Register request for SA."""
        packet = CommonPacket.create_packet(
            sa_dev_type=SADeviceType.REGISTER,
            cmd_type=SACmdType.READ,
            sa_service=SAServiceID.REGISTER,
        )
        resp = self.request(payload=packet.to_pdu())
        return resp

    def read_service(self, sa_service: SAServiceID):
        """Send a Read Service request for SA."""
        packet = CommonPacket.create_packet(
            sa_dev_type=self._sa_type,
            cmd_type=SACmdType.READ,
            sa_service=sa_service,
        )
        resp = self.request(payload=packet.to_pdu())
        return resp

    def write_service(self, sa_service: SAServiceID, value: int):
        """Send a Write Service request for SA."""
        packet = CommonPacket.create_packet(
            sa_dev_type=self._sa_type,
            cmd_type=SACmdType.WRITE,
            sa_service=sa_service,
            value=value
        )
        resp = self.request(payload=packet.to_pdu())
        return resp


__all__ = ['SmartApplication', '_create_payload']
