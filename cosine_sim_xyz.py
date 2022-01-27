# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 09:49:02 2022

@author: alexa
"""
import os
import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt

### this script computes the cosine similarities of all .xyz files within the
### specified directory. the overlap matrix and high overlap cases are printed.

direc = r'D:/Uni/PostDoc/Waterloo/OneDrive - University of Waterloo/1_Ab-Initio/09_Winnipeg_Peptides/GSH/raw_ORCA/'

#### no need to edit beyond this point

a2m = {'H' :  1.,                                                              'He':  4.,
       'Li':  7., 'Be':  9., 'B': 11, 'C': 12., 'N': 14., 'O': 16., 'F' : 19., 'Ne': 20.,
       'Na': 23., 'Mg': 24.,                    'P': 31., 'S': 32., 'Cl': 35., 'Ar': 40.,
       } # from atom label to mass

def parse(file,off=2):
    '''Parse the molecular geometries from a file (.inp, .gjf, .xyz).
    Set off to the number of lines before the geometry starts (e.g. off=2 for .xyz)'''
    f = open(file)
    lines = f.readlines()
    f.close()
    
    mass = []
    xyz = []
    for i in range(off,len(lines)):
        if lines[i].startswith(' '):
            lab, x, y, z = lines[i].split()
            mass.append(a2m[lab])
            xyz.append([float(x), float(y), float(z)])
    
    return np.array(mass), np.array(xyz)

def cos_sim(xyz1,xyz2):
    '''calculates the cosine similarity of two xyz arrays with shape Natx3'''
    Nat = xyz1.shape[0]
    if Nat != xyz2.shape[0]:
        raise ValueError('XYZ files not matching!')
    
    CoM1 = np.sum(mass*xyz1.T,axis=1)/np.sum(mass)
    CoM2 = np.sum(mass*xyz2.T,axis=1)/np.sum(mass)

    R1 = np.array([ mass[i]*LA.norm(xyz1[i,:]-CoM1) for i in range(Nat)])
    R2 = np.array([ mass[i]*LA.norm(xyz2[i,:]-CoM2) for i in range(Nat)])

    s = np.dot(R1,R2)/(LA.norm(R1)*LA.norm(R2))
    if s > 1.:
        s = 1.
    elif s < -1.:
        s = -1.
    
    return 1.-np.arccos(s)/np.pi

################

files = [x for x in os.listdir(direc) if x.lower().endswith('.xyz')]

DAT_xyz = []
for file in files:
    mass, xyz = parse(direc+file,off=2)
    DAT_xyz.append(xyz)

N_conf = len(DAT_xyz)

# overlap matrix
OL_mat = np.zeros((N_conf,N_conf))
for i in range(N_conf):
    for j in range(i,N_conf):
        d = cos_sim(DAT_xyz[i],DAT_xyz[j])
        OL_mat[i,j] = d
        OL_mat[j,i] = d

# plot overlap matrix
plt.matshow(OL_mat)
plt.colorbar()
plt.show()

# print pairs
threshs = np.array([0.995,0.99,0.985,0.98,0.975])
for thmin in threshs:
    thmax = thmin+0.005
    print('\n== similarity between %.3f-%.3f ==' %(thmax,thmin))
    for i in range(N_conf):
        for j in range(i+1,N_conf):
            if OL_mat[i,j] > thmin and OL_mat[i,j] < thmax:
                print('%s and %s   (%.3f)' %(files[i],files[j],OL_mat[i,j]))