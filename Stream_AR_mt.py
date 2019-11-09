#!/usr/bin/env python

import os
import socket
import json
import time

import subprocess
import threading

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class BrainSight2Hololens(StoppableThread):

    def __init__(self, bs_filename, hl_ip=None, hl_port=None):
       super(BrainSight2Hololens, self).__init__()
       self.bs_filename = bs_filename
       self.hl_ip = hl_ip
       self.hl_port = hl_port

    def run(self):
        #os.chdir('/run/user/1000/gvfs/smb-share:server=192.168.1.9,share=brainhack/shared/Gabriel_brain')

        while not self._stop_event.is_set():
            bs_data = self.extract_bs_data()

            if bs_data is None:
                payload = {
                    'data': {},
                    'errorCode': 1,
                    'errorMessage': 'Missing BS data'
                }
            else:
                payload = self.bs_to_payload(bs_data)

            # send to holo
            serialised_payload = json.dumps(payload)
            logger.debug(json.dumps(payload, indent=4))
            if self.hl_ip and self.hl_port:
                self.send(serialised_payload, self.hl_ip, self.hl_port)

    @staticmethod
    def send(data, ip_address='127.0.0.1', port=5005):
        """Send `data` to `ip_address`:`port` via UDP."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(data, (ip_address, port))


    def extract_bs_data(self):
        line = subprocess.check_output(['tail', '-1', self.bs_filename])
        line_cols = line.rstrip().split('\t')
        if line_cols[0] != 'Crosshairs Position':
            return

        # Just copy and paste here the header of the file you want to parse
        file_header = """\
        # Polaris Tool	Date	Time	Polaris Frame Number	Calibration/Tracker Name	Coordinate System	x	y	z	m0n0	m0n1	m0n2	m1n0	m1n1	m1n2	m2n0	m2n1	m2n2
        # TTL Trigger	Date	Time	Trigger Name
        # New Sample	Date	Time	Sample Name	Index	Loc. X	Loc. Y	Loc. Z	m0n0	m0n1	m0n2	m1n0	m1n1	m1n2	m2n0	m2n1	m2n2	Assoc. Target
        # New EMG	Date	Time	Sample Name	Index	EMG Peak-to-peak 1	EMG Peak-to-peak 2	EMG Window Start	EMG Window End
        # Target Selection	Date	Time	Target Name	Loc. X	Loc. Y	Loc. Z	m0n0	m0n1	m0n2	m1n0	m1n1	m1n2	m2n0	m2n1	m2n2
        # Crosshairs Position	Date	Time	Crosshairs Driver	Coordinate System	Loc. X	Loc. Y	Loc. Z	m0n0	m0n1	m0n2	m1n0	m1n1	m1n2	m2n0	m2n1	m2n2"""

        headers = {}
        for header in file_header.split('\n'):
            v = header.lstrip('# ').rstrip().split('\t')
            headers[v[0]] = v

        brain_sight = {}
        for h,v in zip(headers[line_cols[0]], line_cols):
            brain_sight[h] = v

        return brain_sight


    def bs_to_payload(self, bs_data):
        payload = {
            'data': {},
            'errorCode': 0,
            'errorMessage': ''
        }


        for k,v in bs_data.items():
            try:
                # convert to float and change from mm to m (if possible)
                bs_data[k] = float(v) / 1000.
            except ValueError:
                pass

        k = 10.
        payload['data'] = {
            'OrientationPointCone': {
                'UnityX': bs_data['Loc. X'],
                'UnityY': bs_data['Loc. Z'],
                'UnityZ': bs_data['Loc. Y'],
            },
            'EndPointCone': {
                'UnityX': bs_data['Loc. X'] + k * bs_data['m2n0'],
                'UnityY': bs_data['Loc. Z'] + k * bs_data['m2n2'],
                'UnityZ': bs_data['Loc. Y'] + k * bs_data['m2n1'],
            },
            'OrientationPointAxe': {
                'UnityX': bs_data['Loc. X'] + k * bs_data['m1n0'],
                'UnityY': bs_data['Loc. Z'] + k * bs_data['m1n2'],
                'UnityZ': bs_data['Loc. Y'] + k * bs_data['m1n1'],
            },
        }

        return payload


def udp_listen(ip_address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.my_ip, args.my_port))
    data, addr = sock.recvfrom(1024)
    return data


def first_calibration():
    # Implement here your first-time calibration function
    # (feel free to rename the function as you see appropriate)
    pass


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Stream coordinates to HL')
    parser.add_argument('--hl-ip', metavar='ip-address',
                        help='Hololens ip-address')
    parser.add_argument('--hl-port', metavar='port', type=int,
                        help='Hololens port')
    parser.add_argument('--my-ip', metavar='ip-address',
                        help='this localhost ip address on the network (listen)')
    parser.add_argument('--my-port', metavar='port', type=int,
                        help='this localhot port on which to listen')
    parser.add_argument('--input-file', '-i', required=True,
                        help='Brain sight exported file')
    parser.add_argument('--debug', action='store_true',
                        help='enable debug level logging verbosity')
    parser.add_argument('--run-calibration', action='store_true',
                        help='run calibration')
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    if args.run_calibration:
        logger.info('Running calibration...')
        calibration()

    bs2hl = BrainSight2Hololens(bs_filename=args.input_file, hl_ip=args.hl_ip,
                                hl_port=args.hl_port)

    logger.info('Starting BS2HL (sender) Thread...')
    bs2hl.start()

    if args.my_ip and args.my_port:
        logger.info("UDP target IP: %s", args.my_ip)
        logger.info("Listening on UDP port: %s", args.my_port)
        logger.info("Use CTRL-C to stop")
        while True:
            try:
                data = udp_listen(args.my_ip, args.my_port)
            except socket.error as e:
                logger.error('UDP listener error: %s', e)
                break
            logger.info("Received data: %s", data)
    else:
        logger.warning('Not listening')
        logger.info('Starting a simple while loop to not kill the sender...')
        c = ''
        while c != 'q':
            c = raw_input('Enter q to exit: ')
            time.sleep(0.5)


    logger.info('Stopping BS2HL (sender) thread...')
    bs2hl.stop()

    logger.info('Exiting...')
