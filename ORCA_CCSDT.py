'''
Created by CI 2021-04-20

Extractes CCSDT Single point energies directly from ORCA output files
'''
#Where are your ORCA outputs located?
directory = r'H:\Hopkins_Laboratory\Tropylium\ORCA\NEB\OtBu\OtBu_Final1\CCSDT'

###########################################
#No touchy past this point
import os, re

#Generate list of ORCA outputs from directory
filenames = [x for x in os.listdir(directory) if x.lower().endswith('.out')]

#Generate output .csv to write thermochemistry to
opf = open(directory+'//CCSDT_Energies.csv','w')
opf.write('Filename,CCSDT\n')
opf.close()

for filename in filenames:
    
    #open up each ORCA .out file within the directory and read its contents
    opf = open(directory+'//'+filename,'r')
    data = opf.read()
    opf.close()

    #Search for relevant content within datafile
    
    try:
        E_CCSDT = float(re.findall(r'E\(CCSD\(T\)\)                                 ...(.*?)\n',data)[-1].strip())
    except:
        E_CCSDT = float(-12345)


    if float(-12345) in [E_CCSDT]:
        print(str(filename)+' is missing a CCSDT energy. Writing -12345 as placeholder for missing value\n')

    #Append quantities to the thermochemistry .csv
    opf = open(directory+'//CCSDT_Energies.csv','a')
    opf.write('%s,%f\n'%(filename,E_CCSDT))
    opf.close()

print('Done')
