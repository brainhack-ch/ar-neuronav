import socket


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='UDP Sender')
    parser.add_argument('--ip-address', default='127.0.0.1',
                        help='IP address')
    parser.add_argument('--port', '-p', type=int, default=5005,
                        help='UDP port')
    parser.add_argument('--message', default='Hello',
                        help='payload message')
    args = parser.parse_args()

    print "UDP target IP:", args.ip_address
    print "UDP target port:", args.port
    print "message:", args.message


    #while 1==1:
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(args.message, (args.ip_address, args.port))