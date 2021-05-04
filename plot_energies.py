'''
Created by CI 2021-04-16

Script used to plot energies from an Orca SCAN calculation

'''

# Last updated : 2021-04-16

# Get the input file
name = r'H:\Hopkins_Laboratory\Tropylium\ORCA\Benzylium\DFT\pOtBu_Benzylium_1.out'	#directory + name of your output file


#No touchy past here unless you know what you're doing
import re
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

opf = open(name, 'r')
lines = opf.readlines()
opf.close()

# -------------- EXTRACT INFO -------------- #	

Energy = []
for line in lines:
	if re.search('Total Energy       :     ', line):
		temp = line.split()[3]
		Energy.append(temp)
# convert string to float
Energy=[(lambda x: float(x))(x) for x in Energy]
	
# ------------- PLOTTING STUFF ------------- #			
# If only SCF cycle, plot OPTION 1.
# If got passed 1st SCF cycle, plot OPTION 2.
# ------------------------------------------ #	

# OPTION 1:
if Energy != []:

	
	plt.figure()
	
	ax = plt.subplot(111)	
	plt.title('Energy')
	ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
	ax.plot(list(range(1, len(Energy)+1)), Energy, 'r-')
	
plt.show()
