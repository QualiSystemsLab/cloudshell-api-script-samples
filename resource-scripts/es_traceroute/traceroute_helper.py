import socket
from icmplib import traceroute


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


def run_traceroute_to_ip(target_ip: str) -> str:
    tr_hops = traceroute(address=target_ip)
    full_output = "\n".join([str(hop) for hop in tr_hops])
    return full_output


if __name__ == "__main__":
    res = run_traceroute_to_ip("google.com")
    print(res)