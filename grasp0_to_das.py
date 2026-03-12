import read_grasp0
import stg2_lib
import numpy as np 
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file',  help='Specify path of GRASP.INP file')
args = parser.parse_args()

orbital_key = np.array(['s','p','d','f','g','h'])

def main(graspinp):
    nr_peel,occupations = read_grasp0.read_grasp0_inp(graspinp)
    Z = read_grasp0.getNuclearCharge(graspinp)
    orbital_string = ''
    formatOrbitals = '{:>2} {:>2} '
    formatOccupati = '   {:>2} '
    
    occupations = np.transpose(occupations)
    
    namelistAgebDefault = "&SALGEB CUP='IC ' MXVORB= {} MXCONF=  {} KUTSS=-1 KUTSO= 0 KUTOO= 0  &END"
    namelistSminDefault = "&SMINIM NZION= {}   &END"
    
    shape = np.shape(occupations)
    #print(shape)
    norbs = int(shape[1])
    ncsfs = int(shape[0])
    print('A.S.')
    print(namelistAgebDefault.format(norbs,ncsfs))
    for x in nr_peel:
        if len(x) > 2: 
            print('stopping - code this better leo it found an orbital longer than2 characters')
        princ = x[0]
        smallL = np.argwhere(x[1] == orbital_key)[0][0]
        #print(princ,smallL)
        orbital_string += formatOrbitals.format(princ,smallL)
    print(orbital_string)
    
    
    for x in occupations:
        string = ""
        for i in x:
            string+= formatOccupati.format(int(i))
        print(string)
    
    print(namelistSminDefault.format(Z))

    
    
    
    return 0

if not args.file:
    print("No GRASP.INP file specified - assuming GRASP.INP")
    file = 'GRASP.INP'
else:
    file = args.file 

main(graspinp=file)
