#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
UDP_echo program
Solution using python sockets
Student template
"""
import socket
import time
import sys
import statistics


def parse_args() -> tuple[str, int, int, int]:
    """
    parses the 4 args:
    server_hostname, server_port, num_pings, timeout
    """
    # pass  # delete this and write your code
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


def create_socket(timeout: int) -> socket.socket:
    """Create IPv4 UDP client socket"""
    # pass  # delete this and write your code
    # Set socket timeout here.
    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    client_socket.settimeout(timeout)
    return client_socket


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
    loss, rtt_min, rtt_avg, rtt_max, rtt_mdev
    """
    # pass  # delete this and write your code
    loss = (num_pings - len(rtt_hist)) / num_pings * 100 if num_pings > 0 else 0
    rtt_min = min(rtt_hist) if rtt_hist else 0
    rtt_avg = statistics.mean(rtt_hist) if rtt_hist else 0
    rtt_max = max(rtt_hist) if rtt_hist else 0
    rtt_mdev = statistics.stdev(rtt_hist) if len(rtt_hist) > 1 else 0
    return loss, rtt_min, rtt_avg, rtt_max, rtt_mdev


def main() -> None:
    SERVER_HOSTNAME, SERVER_PORT, NUM_PINGS, TIMEOUT = parse_args()
    # Get IP from hostname
    SERVER_IP = socket.gethostbyname(SERVER_HOSTNAME)
    # Create the socket
    client_socket = create_socket(timeout=TIMEOUT)

    # pass  # delete this and write your code
    # Note: you will want exception handling for lost packets (think timeout).
    # round RTT the nearest 10ms before adding it to rtt_hist and displaying it
    rtt_hist = []
    total_time = 0
    ping = False

    for ping_num in range(1, NUM_PINGS + 1):
        # message = f"PING {SERVER_HOSTNAME} ({SERVER_IP}) {ping_num} {time.asctime()}"
        # encoded_message = message.encode()

        message = f"PING {SERVER_HOSTNAME} ({SERVER_IP}) {ping_num} {time.asctime()}"
        if ping == False:
            print(f"PING {SERVER_HOSTNAME} ({SERVER_IP}) {len(message)} bytes of data.")
            ping = True
        try:
            client_socket.sendto(message.encode(), (SERVER_HOSTNAME, SERVER_PORT))

            start_time = time.time()
            response, address = client_socket.recvfrom(1024)
            end_time = time.time()

            rtt = round(
                (end_time - start_time) * 1000
            )  # Convert to milliseconds and round
            total_time += rtt
            rtt_hist.append(float(rtt))  # Append as a float

            if "oops" in response.decode():
                print("Damaged packet")
            else:
                print(
                    f"{len(response)} bytes from {SERVER_HOSTNAME} ({SERVER_IP}): ping_seq={ping_num} time={rtt} ms"
                )

        except socket.timeout:
            print("timed out")

    # ping stats
    loss, rtt_min, rtt_avg, rtt_max, rtt_mdev = net_stats(
        num_pings=NUM_PINGS, rtt_hist=rtt_hist
    )
    # pass  # delete this and write your code
    print(f"\n--- {SERVER_HOSTNAME} ping statistics ---")
    print(
        f"{NUM_PINGS} packets transmitted, {len(rtt_hist)} received, "
        f"{round(loss)}% packet loss, time {int(total_time)}ms"
    )
    print(
        f"rtt min/avg/max/mdev = {int(rtt_min)}/{int(rtt_avg)}/{int(rtt_max)}/{round(rtt_mdev)} ms"
    )


if __name__ == "__main__":
    main()
