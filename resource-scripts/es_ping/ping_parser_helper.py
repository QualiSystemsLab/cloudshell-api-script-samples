import socket
import json
import pingparsing


class PingFailedException(Exception):
    pass


def get_local_ip():
    """
    Use socket to get the local IP, default to loopback 127.0.0.1
    https://stackoverflow.com/a/28950776
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def ping_target_ip(target_ip: str) -> pingparsing.PingStats:
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = target_ip
    transmitter.count = 4
    result = transmitter.ping()
    if result.returncode != 0:
        raise PingFailedException(f"Failed ping output:\n{result.stdout}")
    stats = ping_parser.parse(result)
    if stats.packet_loss_rate > 0:
        stats_json = json.dumps(stats.as_dict(include_icmp_replies=True), indent=4)
        raise PingFailedException(f"Ping loss rate greater than 0.\n{stats_json}")
    return stats


if __name__ == "__main__":
    res = ping_target_ip("google.com").as_dict()
    print(json.dumps(res, indent=4))