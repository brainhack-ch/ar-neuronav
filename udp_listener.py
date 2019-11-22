import socket

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='UDP Listener')
    parser.add_argument('--ip-address', default='127.0.0.1',
                        help='IP address')
    parser.add_argument('--port', '-p', type=int, default=5005,
                        help='UDP port')
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((args.ip_address, args.port))

    print "UDP target IP:", args.ip_address
    print "Listening on UDP port:", args.port

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print "received message:", data