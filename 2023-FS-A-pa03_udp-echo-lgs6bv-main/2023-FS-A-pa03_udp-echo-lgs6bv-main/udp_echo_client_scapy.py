#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
UDP_echo program
Solution using scapy
Solution
"""
import time
import sys
import statistics

from scapy.all import *  # type: ignore

# https://scapy.readthedocs.io/en/latest/troubleshooting.html
conf.L3socket = L3RawSocket  # type: ignore
# sometimes needed for default gateway, and
# always for localhost, and
# sometimes not for remote.


def parse_args() -> tuple[str, int, int, int]:
    """
    parses the 4 args:
    server_hostname, server_port, num_pings, timeout
    """
    # delete this and write (copy from first part)
    if len(sys.argv) != 5:
        print(
            "Usage: python3 udp_echo_client.py <server hostname> <server port> <num pings> <timeout in sec>"
        )
        sys.exit(1)
    server_hostname, server_port, num_pings, timeout = (
        sys.argv[1],
        int(sys.argv[2]),
        int(sys.argv[3]),
        int(sys.argv[4]),
    )
    return server_hostname, server_port, num_pings, timeout


def net_stats(
    num_pings: int, rtt_hist: list[float]
) -> tuple[float, float, float, float, float]:
    """
    Computes statistics for loss and timing.
    Mimicks the real ping's statistics.
    Check them out: `ping 127.0.0.1`
    See `man ping` for definitions.
    This is just a math function.
    Don't do any networking here.
    """
    # delete this and write (copy from first part)
    loss = (num_pings - len(rtt_hist)) / num_pings * 100 if num_pings > 0 else 0
    rtt_min = min(rtt_hist) if rtt_hist else 0
    rtt_avg = statistics.mean(rtt_hist) if rtt_hist else 0
    rtt_max = max(rtt_hist) if rtt_hist else 0
    rtt_mdev = statistics.stdev(rtt_hist) if len(rtt_hist) > 1 else 0
    return loss, rtt_min, rtt_avg, rtt_max, rtt_mdev


def main() -> None:
    SERVER_HOSTNAME, SERVER_PORT, NUM_PINGS, TIMEOUT = parse_args()
    # Get IP from hostname
    # delete this and write (copy most, but not all, from first part)
    return


if __name__ == "__main__":
    main()
