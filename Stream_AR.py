#!/usr/bin/env python

import os
import socket
import json
import numpy as np
import pandas as pd


class StreamBaseError(Exception):

    error_code = 1
    error_message = "Steam Error"


class UmbrellaOutsideError(StreamBaseError):

    error_code = 2
    error_message = "Umbrella outside field of view"


def send(data, ip_address='127.0.0.1', port=5005):
    """Send `data` to `ip_address`:`port` via UDP."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (ip_address, port))


def extract_coordinates(filename):
    a = pd.read_csv(filename, skiprows=5, sep='\t')
    afull = a[['Coordinate System', 'x', 'y', 'z', 'm0n0', 'm0n1', 'm0n2',
               'm1n0', 'm1n1', 'm1n2', 'm2n0', 'm2n1', 'm2n2']]
    af = afull.as_matrix()

    #Create a vector with the last value of the file
    q = af[len(af)-1: , 0:3 ]
    m0 = af[len(af)-1: ,3:6]
    m1 = af[len(af)-1: ,6:9]
    m2 = af[len(af)-1: ,9:12]

    if q[0,0] == 'NIfTI:Scanner':
        raise UmbrellaOutsideError()

    # Note: will divide by 1000. to go from mm to m

    q = [float(i) / 1000. for i in q[0]]
    #print(q)

    '''
    c=pd.read_csv('Brainhack_stream2.txt')
    chead=c.head(10)
    ctail=c.tail(1)
    c = [chead, ctail]
    c = pd.concat(c)
    c.to_csv('Brainhack_stream2.txt', header=None, index=None, sep='	', mode='a')
    '''

    #Convert the coordinates of the dot into brain space
    #print(np.dot(R,q)+T)
    #trans_q=np.dot(R,q)+T

    # convert angles into brain space
    m0 = [float(i) / 1000. for i in m0[0]]
    #trans_m0=np.dot(R,m0)

    m1 = [float(i) / 1000. for i in m1[0]]
    #trans_m1=np.dot(R,m1)

    m2 = [float(i) /1000. for i in m2[0]]
    #trans_m2=np.dot(R,m2)

    return q, m0, m1, m2


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Stream coordinates to HL')
    parser.add_argument('--hl-ip', metavar='ip-address',
                        help='Hololens ip-address')
    parser.add_argument('--hl-port', metavar='port', type=int,
                        help='Hololens port')
    parser.add_argument('--input-file', required=True,
                        help='Brain sight exported file')
    args = parser.parse_args()


    #os.chdir('/run/user/1000/gvfs/smb-share:server=192.168.1.9,share=brainhack/shared/Gabriel_brain')

    while True:
        # default values
        payload = {
            'data': {},
            'errorCode': 0,
            'errorMessage': ''
        }


        try:
            q, m0, m1, m2 = extract_coordinates(args.input_file)
        except StreamBaseException as e:
            payload['errorCode'] = e.error_code
            payload['errorMessage'] = e.error_message

        # save to file
        #np.savetxt('/home/oreynaud/Desktop/Brainhack/data/update_pts.txt', q)
        #np.savetxt('/home/oreynaud/Desktop/Brainhack/data/update_angleX.txt', m0)
        #np.savetxt('/home/oreynaud/Desktop/Brainhack/data/update_angleY.txt', m1)
        #np.savetxt('/home/oreynaud/Desktop/Brainhack/data/update_angleZ.txt', m2)

        if payload['errorCode'] == 0:
            k = 10.
            payload['data'] = {
                'OrientationPointCone': {
                    'UnityX': q[0],
                    'UnityY': q[2],
                    'UnityZ': q[1],
                },
                'EndPointCone': {
                    'UnityX': q[0] + k * m2[0],
                    'UnityY': q[2] + k * m2[2],
                    'UnityZ': q[1] + k * m2[1],
                },
                'OrientationPointAxe': {
                    'UnityX': q[0] + k * m1[0],
                    'UnityY': q[2] + k * m1[2],
                    'UnityZ': q[1] + k * m1[1],
                },
            }


        # send to holo
        serialised_payload = json.dumps(payload)
        #print(serialised_payload)
        if args.hl_ip and args.hl_port:
            send(serialised_payload, args.hl_ip, args.hl_port)



        # definition of 3 points in brain space that must go to unity base after transformation
        #X=[trans_m0[0]+trans_q[0],trans_m0[1]+trans_q[1],trans_m0[2]+trans_q[2]] #location M+x --> x'=1,0,0
        #Y=[trans_m1[0]+trans_q[0],trans_m1[1]+trans_q[1],trans_m1[2]+trans_q[2]] #location M+y --> y'=0,1,0
        #Z=[trans_m2[0]+trans_q[0],trans_m2[1]+trans_q[1],trans_m2[2]+trans_q[2]] #location M+z --> z'=0,0,1

        # calculate rotation matrix and save it locally
        #vector_brain=np.array([X,Y,Z])
        #M=superimposition_matrix(vector_brain.T, vector_tms.T, scale=True, usesvd=False)
        #M2 = [M[0][0], M[0][1], M[0][2]],[M[1][0], M[1][1], M[1][2]],[M[2][0], M[2][1], M[2][2]],[M[0][3], M[1][3], M[2][3]]
        #np.savetxt('/home/oreynaud/Desktop/Brainhack/data/stream_ROTMAT_Brain2TMS.txt',M2,fmt='%10.6f')
