'''
Created by CI 2021-05-17
Converts Gaussian output files (.log) files to ORCA input files
'''

#Where are your xyz files located?
directory = r'D:\OneDrive\OneDrive - University of Waterloo\Waterloo\PhD\Manuscripts\2021\Mat_Comm_Today_Letter\Zimincka_structures\bCD_Atropine\Ziminicka\New folder'

#Important things for the input block
calc_line = '! wB97X-D3 Opt Freq def2-TZVPP def2/J RIJCOSX TightSCF CHELPG'  #Must be a string
#calc_line = '! DLPNO-CCSD(T) def2-TZVPP def2-TZVPP/C TightSCF  '  #Must be a string
mpp = 8192  #Memory per processor in MB. Keep in increments of n*1024 otherwize orca gets confused
ncores = 1  #Number of cores to use in the calculation 
charge = 1  #What is the charge?
multiplicity = 1    #What is the multiplicity?

#ESP Charges
ESP_Charges = True  #Do you want custom parameters in the ChelpG scheme? 
grid = 0.1 #Default is 0.3
rmax = 3.0 #Default is 2.8

###########################################################################
#No touchy past this point

import os, re
from Atom_Info import *

#Generate directory to write new files to
try:
    new_dir = os.mkdir(directory+'\\New_Inputs')
except FileExistsError:
    pass #if folder already exists, do nothing

#Generate list of ORCA outputs from directory excluding xyz files that are trajectories from an optimization
filenames = [x for x in os.listdir(directory) if x.lower().endswith('.log')]

############################
#Create ORCA file
############################
for filename in filenames:
    opf = open(directory+'\\New_Inputs\\'+filename[:-4]+'.inp','w')

#Input block    
    if calc_line.startswith('!') == True:
        opf.write(calc_line+'\n')
    else:
        print('The input line in '+filename+' does not start with a ! Adding it in now')
        calc_line = '! '+calc_line
        opf.write(calc_line+'\n')

#Memory    
    if mpp % 1024 == 0:
        opf.write('%maxcore '+str(mpp)+'\n\n')
    else:
        print('The memory (mpp) specified is not divisible by 1024. Fixing it now')
        x = int(mpp / 1024)
        mpp = int(1024*x)
        opf.write('%maxcore '+str(mpp)+'\n\n')

#Number of cores    
    if isinstance(ncores, int) == True:
        opf.write('%pal nprocs '+str(ncores)+' \nend\n\n')
    else:
        print('The number of cores specified is not an integer. You cannot have factional CPUs! Fixing it now')
        ncores = (round(ncores))
        opf.write('%pal nprocs '+str(ncores)+' \nend\n\n')

#ESP Charges
    if ESP_Charges == True:
        opf.write(r'%chelpg'+'\n')
        opf.write('grid '+str(grid)+'\n')
        opf.write('rmax '+str(rmax)+'\n')
        opf.write('end\n\n\n')

#File block
    opf.write('* xyzfile '+str(charge)+' '+str(multiplicity)+' '+str(filename)[:-4]+'.xyz\n\n\n\n')
    opf.close()

############################
#Create xyz file from .log
############################

    opf = open(directory+'\\'+filename,'r')
    data = opf.read()
    opf.close()

    #Get the geometry and write to list called geoemtry
    geometry=[] #Get geometry of atoms from file
    GEOM = re.findall(r'Standard orientation([\s\S]*?)Rotational constants',data)
    if len(GEOM) == 0: #Sometime frequency calculations are missing above block
        GEOM = re.findall(r'Axes restored to original set([\s\S]*?)Cartesian Forces',data)
    if len(GEOM) > 0:
        geometry = []
        for i in GEOM[-1].split('\n')[5:-2]:
            i = i.split()
            if len(i) == 6:
                geometry.append([chemical_symbols[int(i[1])],i[3],i[4],i[5]])
            else:
                geometry.append([chemical_symbols[int(i[1])],i[2],i[3],i[4]])

    #Write the geometry to a formatted string
    fs = ''
    for i in geometry:
        fs+='%2s    %12s    %12s    %12s\n'%(i[0],i[1],i[2],i[3])    

    #At long last, we can write all the info to the .xyz file
    opf = open(directory+'\\New_Inputs\\'+filename[:-4]+'.xyz','w')
    opf.write(str(len(geometry))+'\n\n')
    opf.write(fs)
    opf.write('\n')
    opf.close()

print('Done')
