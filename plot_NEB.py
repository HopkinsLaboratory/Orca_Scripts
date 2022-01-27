# -*- coding: utf-8 -*-
"""
Script to read in ORCA NEB calculation and plot data.

Created on Wed Jan 26 17:07:00 2022

@author: Alexander Haack
"""

import os
import numpy as np
import matplotlib.pyplot as plt

def dist(xyz1,xyz2):
    '''calcualtes the distance between two 3N vectors'''
    return np.linalg.norm(xyz1-xyz2)

def read_path(filename):
    f = open(direc+file)
    lines = f.readlines()
    f.close()
    
    Nat = int(lines[0])
    IMs = [] # list of image class instances
    
    ## read in data
    i=0
    while lines[i].startswith(str(Nat)):
        E = float(lines[i+1].split()[-1])
        atoms = []
        xyz = []
        for j in range(Nat):
            at, x, y, z = lines[i+2+j].split()
            atoms.append(at)
            xyz.append([float(x), float(y), float(z)])
        IMs.append(Imag(atoms,np.array(xyz),E))
        i += Nat+2
        if i >= len(lines):
            break
        
    return path(IMs) # return path class instance

class Imag:
    '''Class for single image of the path'''
    def __init__(self,atoms,xyz,E):
        '''atom labels (list of strings), coordinates (Nx3 dim np.array), energy (float)'''
        self.atoms = atoms
        self.xyz = xyz
        self.E = E
    
    def as_3N(self):
        '''returns Nx3 xyz array as 3N array'''
        return np.hstack(self.xyz)
    
    def R(self,i,j):
        '''calculates distance between atoms i and j (counting from 0)'''
        return np.linalg.norm(self.xyz[i]-self.xyz[j])

    def A(self,i,j,k):
        '''calculates the angle formed by atoms i-j-k (counting from 0)'''
        v1 = self.xyz[i] - self.xyz[j]
        v2 = self.xyz[k] - self.xyz[j]
        return np.degrees(np.arccos(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))))
    
    def D(self,i,j,k,l):
        '''calculates the dighedral formed by atoms i-j-k-l (counting from 0)'''
        # http://azevedolab.net/resources/dihedral_angle.pdf
        # three plane defining vectors
        q1 = self.xyz[i] - self.xyz[j]
        q2 = self.xyz[k] - self.xyz[j]
        q3 = self.xyz[l] - self.xyz[k]
        # normal vectors of two planes
        n1 = np.cross(q1,q2) / np.linalg.norm(np.cross(q1,q2))
        n2 = np.cross(-q2,q3) / np.linalg.norm(np.cross(-q2,q3))
        # orthogonal unity vectors
        u1 = n2
        u3 = q2/np.linalg.norm(q2)
        u2 = np.cross(u3,u1)
        # dihedral via theta=-atan2(n1*u2/n1*u1)
        return -np.degrees(np.math.atan2(np.dot(n1,u2),np.dot(n1,u1)))

## end of image class

class path:
    '''Class of the MEP'''
    def __init__(self,IMs):
        self.IMs = IMs
        self.Nim = len(self.IMs)
        E = np.array([x.E for x in self.IMs])
        self.E = E-E.min()
        self.d = np.array([dist(self.IMs[0].as_3N(), self.IMs[i].as_3N()) for i in range(self.Nim) ])
        
        self.HEI = np.argmax(self.E)
        self.atoms = self.IMs[0].atoms
    
    def lab(self,*ind):
        llist = []
        for i in ind:
            llist.append(self.atoms[i])
            llist.append('$_{%i}$' %i)
            llist.append(',')
        label = '%s%s%s'*len(ind) %(*llist,)
        return label[:-1]
    
    def get_R(self,i,j):
        return np.array([IM.R(i,j) for IM in self.IMs])

    def get_A(self,i,j,k):
        return np.array([IM.A(i,j,k) for IM in self.IMs])

    def get_D(self,i,j,k,l,modulo=True):
        if modulo:
            D_path = np.array([IM.D(i,j,k,l)%360 for IM in self.IMs])
        else:
            D_path = np.array([IM.D(i,j,k,l) for IM in self.IMs])
        return D_path
    
    def plot(self,X,Y,xlab,ylab):
        '''plots X versus Y with respective labels'''
        if len(X) != len(Y):
            raise ValueError('X and Y arrays are not matching!')
        plt.figure(figsize=(6,6))
        plt.plot(X, Y, 'kx-', label='MEP')
        plt.plot(X[self.HEI], Y[self.HEI], 'rx', ms=15, label='HEI (Im_%i)' %self.HEI)
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.legend()
        plt.show()
    
    def plot_EvDist(self):
        '''Plot energy versus distance between images'''
        self.plot(self.d,self.E,r'distance / $\AA$',r'rel. energy / $E_h$')

    def plot_EvR(self,i,j):
        '''Plot energy versus R(i,j) (counting from 0)'''
        self.plot(self.get_R(i,j),self.E,
                  r'R(%s) / $\AA$' %self.lab(i,j),r'rel. energy / $E_h$')
        
    def plot_EvA(self,i,j,k):
        '''Plot energy versus A(i,j,k) (counting from 0)'''
        self.plot(self.get_A(i,j,k),self.E,
                  r'A(%s) / degrees' %self.lab(i,j,k),r'rel. energy / $E_h$')
        
    def plot_EvD(self,i,j,k,l,modulo=True):
        '''Plot energy versus D(i,j,k,l) (counting from 0)'''
        self.plot(self.get_D(i,j,k,l,modulo=modulo),self.E,
                  r'D(%s) / degrees' %self.lab(i,j,k,l),r'rel. energy / $E_h$')
    
    def plot_RvDist(self,i,j):
        '''plot R(i,j) vs path progression (counting from 0)'''
        self.plot(self.d,self.get_R(i,j),r'distance / $\AA$',r'R(%s) / $\AA$' %self.lab(i,j))
    
    def plot_AvDist(self,i,j,k):
        '''plot A(i,j,k) vs path progression (counting from 0)'''
        self.plot(self.d,self.get_A(i,j,k),
                  r'distance / $\AA$',r'A(%s) / degrees' %self.lab(i,j,k))
    
    def plot_DvDist(self,i,j,k,l,modulo=True):
        '''plot D(i,j,k,l) vs path progression (counting from 0)'''
        self.plot(self.d,self.get_D(i,j,k,l,modulo=modulo),
                  r'distance / $\AA$',r'D(%s) / degrees' %self.lab(i,j,k,l))

## end of path class

#######################################################################################
##  You only need to edit stuff here!                                                ##
##  Define directory and filename of the name_MEP_trj.xyz file                       ##
##  The name_MEP_trj.xyz file is created after each NEB iteration.                   ##
##  The calculation does not need to be finished to use this script!                 ##
##                                                                                   ##
##  At the bottom, you can pre-define plots:                                         ##
##                                                                                   ##
##  MEP.plot_EvDist()        - plots energy vs. path length                          ##
##  MEP.plot_EvR(i,j)        - plots energy vs. bond distance between atoms i-j      ##
##  MEP.plot_EvA(i,j,k)      - plots energy vs. angle between atoms i-j-k            ##
##  MEP.plot_EvD(i,j,k,l)    - plots energy vs. dihedral between atoms i-j-k-l       ##
##  MEP.plot_RvDist(i,j)     - plots bond distance between atoms i-j vs. path length ##
##  MEP.plot_AvDist(i,j,k)   - plots angle between atoms i-j-k vs. path length       ##
##  MEP.plot_DvDist(i,j,k,l) - plots dihedral between atoms i-j-k-l vs. path length  ##
##                                                                                   ##
##  All atom numbers i,j,k,l are counted starting from 0                             ##
##  You can also type these commands into the console.                               ##
##  Plots will show the path as well as the highest energy image (HEI)               ##
##                                                                                   ##
##  The MEP class also provides other functions. You can get the plotted arrays with ##
##                                                                                   ##
##  MEP.E              - returns an array with E along the path                      ##
##  MEP.get_R(i,j)     - returns an array with R(i,j) along the path                 ##
##  MEP.get_A(i,j,k)   - returns an array with A(i,j,k) along the path               ##
##  MEP.get_D(i,j,k,l) - returns an array with D(i,j,k,l) along the path             ##
#######################################################################################

direc = r'D:/Uni/PostDoc/Waterloo/OneDrive - University of Waterloo/1_Ab-Initio/09_Winnipeg_Peptides/GGG/NEBs/c2a/'
file = 'GGG-H_c2a_NEB-CI_MEP_trj.xyz'

MEP = read_path(direc+file) # don't change this

## plotting of path in different projections. some examples:
MEP.plot_EvDist()
#MEP.plot_EvR(13,16)
#MEP.plot_EvA(14,15,21)
MEP.plot_EvD(13,10,14,16,modulo=True)
#MEP.plot_DvDist(13,10,14,16,modulo=True)
