#!/usr/bin/env python

import os
import socket
import json
import numpy as np
import pandas as pd
from transformations import random_vector, rotation_matrix, \
                            angle_between_vectors, vector_product, \
                            unit_vector, superimposition_matrix, \
                            translation_from_matrix, decompose_matrix


def send(data, ip_address='127.0.0.1', port=5005):
    """Send `data` to `ip_address`:`port` via UDP."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (ip_address, port))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Stream coordinates to HL')
    parser.add_argument('--hl-ip', metavar='ip-address', required=True,
                        help='Hololens ip-address')
    parser.add_argument('--hl-port', metavar='port', type=int, required=True,
                        help='Hololens port')
    args = parser.parse_args()


    os.chdir('/run/user/1000/gvfs/smb-share:server=192.168.1.9,share=brainhack/shared/Gabriel_brain')

    while True:

        a = pd.read_csv('Brainhack_stream2.txt', skiprows=5, sep='\t')
        a1 = a[['x', 'y', 'z']]
        a2 = a1.as_matrix()

        afull = a[['x', 'y', 'z', 'm0n0', 'm0n1', 'm0n2', 'm1n0', 'm1n1',
                   'm1n2', 'm2n0', 'm2n1', 'm2n2']]
        af = afull.as_matrix()

        #Create a vector with the last value of the file
        q = a2[len(a2)-1: , : ]
        m0 = af[len(af)-1: ,3:6]
        m1 = af[len(af)-1: ,6:9]
        m2 = af[len(af)-1: ,9:12]

        if q[0,1] == "(null)":
            print("Umbrella outside field of view")
            continue

        q = q[0]
        q = [float(i) for i in q]
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
        np.savetxt('/home/oreynaud/Desktop/Brainhack/data/update_pts.txt', q)

        # convert angles into brain space
        m0 = m0[0]
        m0 = [float(i) for i in m0]
        #trans_m0=np.dot(R,m0)
        np.savetxt('/home/oreynaud/Desktop/Brainhack/data/update_angleX.txt', m0)

        m1 = m1[0]
        m1 = [float(i) for i in m1]
        #trans_m1=np.dot(R,m1)
        np.savetxt('/home/oreynaud/Desktop/Brainhack/data/update_angleY.txt', m1)

        m2 = m2[0]
        m2 = [float(i) for i in m2]
        #trans_m2=np.dot(R,m2)
        np.savetxt('/home/oreynaud/Desktop/Brainhack/data/update_angleZ.txt', m2)


        data = {
            'q': {
                'x': q[0],
                'y': q[1],
                'z': q[2]
            },
            'm0': {
                'n0': m0[0],
                'n1': m0[1],
                'n2': m0[2],
            }
        }

        serialised_data = json.dump(data)
        send(serialised_data, args.hl_ip, args.hl_port)


        # definition of 3 points in brain space that must go to unity base after transformation
        #X=[trans_m0[0]+trans_q[0],trans_m0[1]+trans_q[1],trans_m0[2]+trans_q[2]] #location M+x --> x'=1,0,0
        #Y=[trans_m1[0]+trans_q[0],trans_m1[1]+trans_q[1],trans_m1[2]+trans_q[2]] #location M+y --> y'=0,1,0
        #Z=[trans_m2[0]+trans_q[0],trans_m2[1]+trans_q[1],trans_m2[2]+trans_q[2]] #location M+z --> z'=0,0,1

        # calculate rotation matrix and save it locally
        #vector_brain=np.array([X,Y,Z])
        #M=superimposition_matrix(vector_brain.T, vector_tms.T, scale=True, usesvd=False)
        #M2 = [M[0][0], M[0][1], M[0][2]],[M[1][0], M[1][1], M[1][2]],[M[2][0], M[2][1], M[2][2]],[M[0][3], M[1][3], M[2][3]]
        #np.savetxt('/home/oreynaud/Desktop/Brainhack/data/stream_ROTMAT_Brain2TMS.txt',M2,fmt='%10.6f')
