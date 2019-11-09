
import os
import sys
import numpy as np
import pandas as pd
from transformations import random_vector,rotation_matrix,angle_between_vectors,vector_product,unit_vector,superimposition_matrix,translation_from_matrix,decompose_matrix




#os.chdir('/home/brainhacker/tms-tracto/tms-tracto/')
#os.chdir('/run/user/1000/gvfs/smb-share:server=192.168.1.9,share=brainhack/shared/Gabriel_brain')

# definition of tms space as target
#Xp=[1,0,0]
#Yp=[0,1,0]
#Zp=[0,0,1] 
#vector_tms=np.array([Xp,Yp,Zp])

# fetch rotation matrix (brainsight units to brain)
#K=np.loadtxt('ROTMAT.txt')
#R1 = K[0][0],K[0][1],K[0][2]
#R2 = K[1][0],K[1][1],K[1][2]
#R3 = K[2][0],K[2][1],K[2][2]
#Translation  = K[3][0],K[3][1],K[3][2]	
#R = np.array([R1,R2,R3]) # rotation matrix
#T = np.array(Translation) # extra translation

while (1==1):

    a=pd.read_csv('Brainhack_stream2.txt',skiprows=5,sep='\t')
    #print(a)



    afull=a[['Coordinate System','x','y','z','m0n0','m0n1','m0n2','m1n0','m1n1','m1n2','m2n0','m2n1','m2n2']]
    af=afull.as_matrix()
    #print(af)

    #Create a vector with the last value of the file
    q=af[len(af)-1: , 0:3 ]
    m0=af[len(af)-1: ,3:6]
    m1=af[len(af)-1: ,6:9]
    m2=af[len(af)-1: ,9:12]
    
    #print(q)
    #print(q[0,0])

    if (q[0,0] == 'NIfTI:Scanner'):
        print("Umbrella outside field of view")
    else:
        q=q[0]
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
        np.savetxt('C:\Users\oreynaud\Desktop\Brainhack\data\update_pts2.txt',q)

        # convert angles into brain space
        m0 = m0[0]
        m0 = [float(i) for i in m0]
        #trans_m0=np.dot(R,m0)
        np.savetxt('C:\Users\oreynaud\Desktop\Brainhack\data\update_angleX2.txt',m0)

        m1 = m1[0]
        m1 = [float(i) for i in m1]
        #trans_m1=np.dot(R,m1)
        np.savetxt('C:\Users\oreynaud\Desktop\Brainhack\data\update_angleY2.txt',m1)

        m2 = m2[0]
        m2 = [float(i) for i in m2]
        #trans_m2=np.dot(R,m2)
        np.savetxt('C:\Users\oreynaud\Desktop\Brainhack\data\update_angleZ2.txt',m2)


        # definition of 3 points in brain space that must go to unity base after transformation
        #X=[trans_m0[0]+trans_q[0],trans_m0[1]+trans_q[1],trans_m0[2]+trans_q[2]] #location M+x --> x'=1,0,0
        #Y=[trans_m1[0]+trans_q[0],trans_m1[1]+trans_q[1],trans_m1[2]+trans_q[2]] #location M+y --> y'=0,1,0
        #Z=[trans_m2[0]+trans_q[0],trans_m2[1]+trans_q[1],trans_m2[2]+trans_q[2]] #location M+z --> z'=0,0,1

        # calculate rotation matrix and save it locally
        #vector_brain=np.array([X,Y,Z])
        #M=superimposition_matrix(vector_brain.T, vector_tms.T, scale=True, usesvd=False)
        #M2 = [M[0][0], M[0][1], M[0][2]],[M[1][0], M[1][1], M[1][2]],[M[2][0], M[2][1], M[2][2]],[M[0][3], M[1][3], M[2][3]]
        #np.savetxt('/home/oreynaud/Desktop/Brainhack/data/stream_ROTMAT_Brain2TMS.txt',M2,fmt='%10.6f')




    #system sleep?
