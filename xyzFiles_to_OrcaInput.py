'''
Created by CI 2021-04-26 [Happy birthday to me :)]

Extractes CCSDT Single point energies directly from ORCA output files
'''
#Where are your xyz files located?
directory = r'H:\Hopkins_Laboratory\Tropylium\ORCA\Tropylpyridinium\DFT'

#Important things for the input block
calc_line = '! DLPNO-CCSD(T) def2-TZVPP def2-TZVPP/C TightSCF  '  #Must be a string
mpp = 8192  #Memory per processor in MB. Keep in increments of n*1024 otherwize orca gets confused
ncores = 1  #Number of cores to use in the calculation 
charge = 1  #What is the charge?
multiplicity = 1    #What is the multiplicity?


##########################################################################
#No touchy past this point

import os
from shutil import copyfile

#Generate directory to write new files to
try:
    new_dir = os.mkdir(directory+'\\New_Inputs')
except FileExistsError:
    pass #if folder already exists, do nothing

#Generate list of ORCA outputs from directory excluding xyz files that are trajectories from an optimization
filenames = [x for x in os.listdir(directory) if x.lower().endswith('.xyz') and '_trj' not in x]

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

#File block
    opf.write('* xyzfile '+str(charge)+' '+str(multiplicity)+' '+str(filename)+'\n\n\n\n')
    opf.close()

#Copy xyz file to new directory
    copyfile(directory+'\\'+filename,directory+'\\New_Inputs\\'+filename)

print('Done')
