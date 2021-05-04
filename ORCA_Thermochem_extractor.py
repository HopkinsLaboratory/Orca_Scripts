'''
Created by CI 2021-04-15

Extractes thermochemical qunatities directly from ORCA output files
'''
#Where are your ORCA outputs located?
directory = r'H:\Hopkins_Laboratory\Tropylium\ORCA\NEB\OtBu\OtBu_Final1'

import os, re, sys


#Generate list of ORCA outputs from directory
filenames = [x for x in os.listdir(directory) if x.lower().endswith('.out')]

#Generate output .csv to write thermochemistry to
try:
    opf = open(directory+'//Thermo_data.csv','w')
    opf.write('Filename,Electronic energy,ZPE Corr,Thermal Corr,H corr,G corr,ZPE Energy,Thermal Energy,Enthalpy,Entropy,Gibbs\n')
    opf.close()
except PermissionError:
    print('A file with the same name is already open. Close it and rerun the code')
    sys.exit()

for filename in filenames:
    
    #open up each ORCA .out file within the directory and read its contents
    opf = open(directory+'//'+filename,'r')
    data = opf.read()
    opf.close()

    #Search for relevant content within datafile
    
    try:
        E_el = float(re.findall('FINAL SINGLE POINT ENERGY(.*?)\n',data)[-1].strip())
    except:
        E_el = float(-12345)
    try:
        ZPE_corr = float(re.findall('Zero point energy                ...(.*?)Eh',data)[-1].strip())
    except:
        ZPE_corr = float(-12345)
    try:
        Thermal_corr = float(re.findall('Total thermal correction(.*?)Eh',data)[-1].strip())
    except:
        Thermal_corr = float(-12345)
    try:
        H_corr = float(re.findall('Thermal Enthalpy correction       ...(.*?)Eh',data)[-1].strip())
    except:
        H_corr = float(-12345)
    try:
        S_tot = float(re.findall('Final entropy term                ...(.*?)Eh',data)[-1].strip())
    except:
        S_tot = float(-12345)
    try:
        G_corr = float(re.findall(r'G-E\(el\)                           ...(.*?)Eh',data)[-1].strip())
    except:
        G_corr = float(-12345)
    try:
        E_thermal = float(re.findall('Total thermal energy(.*?)Eh',data)[-1].strip())
    except:
        E_thermal = float(-12345)
    try:
        E_Enthalpy = float(re.findall('Total Enthalpy                    ...(.*?)Eh',data)[-1].strip())
    except:
        E_Enthalpy = float(-12345)    
    try:
        E_Gibbs = float(re.findall('Final Gibbs free energy         ...(.*?)Eh',data)[-1].strip())
    except:
        E_Gibbs = float(-12345)        
    try:
        E_ZPE = float(E_el) + float(ZPE_corr)
    except:
        E_ZPE = float(-12345)

    if float(-12345) in [E_el,ZPE_corr,Thermal_corr,H_corr,G_corr,E_ZPE,E_thermal,E_Enthalpy,S_tot,E_Gibbs]:
        print(str(filename)+' is missing thermochemistry. Writing -12345 as placeholder for missing value\n')

    #Append quantities to the thermochemistry .csv
    opf = open(directory+'//Thermo_data.csv','a')
    opf.write('%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n'%(filename,E_el,ZPE_corr,Thermal_corr,H_corr,G_corr,E_ZPE,E_thermal,E_Enthalpy,S_tot,E_Gibbs))
    opf.close()

print('Done')
