'''

Created by CI 2021-04-15

Calculates thermochemical corrections from vibrational frequencies as read from ORCA output files
Requires installation of thermoanalysis script. See https://github.com/eljost/thermoanalysis

'''

#Where are your ORCA outputs located?
directory = r'H:\Hopkins_Laboratory\Tropylium\ORCA\Alcohols\DFT'

#Where is your thermo script located?
thermo = r'C:\Python37\Scripts\thermo.exe'

#Code Parameters
Temp = 298.15   #Temperautre(s) in Kelvin
Pressure = 101325   #Pressure in Pascal (1 atm)
vibs = 'qrrho'  #Grimmes QRRHO approach OR a purely harmonic rrho. Usage is simply 'rrho'. qrrho is reccomended
scale = 1.00    #Scaling factor for vib frequencies. LEave as 1.00 unless you know what you're doing

import subprocess
import h5py, numpy, pytest, tabulate, os

#Generate output .csv to write thermochemistry to
opf = open(directory+'//Thermo_data_Calculated.csv','w')
opf.write('Filename,Temperature,Pressure,Electronic energy,Thermal Corr,Thermal Energy,Total Enthalpy,T*S_tot,Gibbs Energy,Gibbs Corr\n')
opf.close()

#Generate list of ORCA outputs
filenames = [x for x in os.listdir(directory) if x.lower().endswith('.out')]

for filename in filenames:
    try:
        result = subprocess.run([(thermo), (directory+'\\'+filename),('--temp'),(str(Temp)),('--pressure'),(str(Pressure)),('--vibs'),(vibs),('--scale'),(str(scale))],stdout=subprocess.PIPE)
        output = (result.stdout.decode('utf-8').split('\r\n')[-2]).split('  ')
    except:
        print('Problem with '+str(filename)+' or parameters. See documentation of thermo.exe. Skipping file and moving to next')
        pass

    opf = open(directory+'//Thermo_data_Calculated.csv','a')
    opf.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n'%(filename,output[0],output[1],output[2],output[3],output[4],output[5],output[6],output[7],output[8]))
    opf.close()    



