import read_grasp0
import stg2_lib
import numpy as np 
import argparse

#right now this code assumes that your orbitals follow the standard order, at least
#in the beginning.

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file',  help='Specify path of GRASP.INP file')
parser.add_argument('-n', '--num',  help='num cont.orbs  ',type=int)
parser.add_argument('-k', '--kappa',  help='max kappa value',type=int)


args = parser.parse_args()

orbital_key = np.array(['s','p','d','f','g','h'])

orbital_key = 'spdfghjklmnopq'

def main(graspinp):
    nr_peel,occupations = read_grasp0.read_grasp0_inp(graspinp)
    Z = read_grasp0.getNuclearCharge(graspinp)
    orbital_string = ''
    formatOrbitals = '{:>2} {:>2} '
    formatOccupati = '   {:>2} '
    #print(nr_peel)
    
    foundSmallL = []
    foundSmallLInt = []
    maxNforEachL = []
    for orb in nr_peel:
        ll = orb[-1]
        nn = int(orb[:-1])
        if not( ll in foundSmallL):
            foundSmallL.append(ll)
            foundSmallLInt.append(orbital_key.index(ll))
            maxNforEachL.append(nn)
        else:
            thisIndex = foundSmallL.index(ll)
            if nn > maxNforEachL[thisIndex]:
                maxNforEachL[thisIndex] = nn
            
    #print(foundSmallLInt)
    nelectrons = int(np.sum(occupations[:,0]))
    
    kbmax = int ( 2* max(foundSmallLInt) + 1)
    
    #print(maxNforEachL)
    
    maxNString = ' {:2}'.format(maxNforEachL[0])
    for ii in range(1,len(maxNforEachL)):
        maxNString += ' {:2}'.format(maxNforEachL[ii])
        maxNString += ' {:2}'.format(maxNforEachL[ii])
    maxNString += '\n'
    
    oo = open('ORBS.INP','w')
    
    oo.write(" DSTG1 : \n") 
    oo.write(" &ORBS\n")
    oo.write(f" KBMAX = {kbmax} \n")
    oo.write(" KCMIN = 1\n")
    oo.write(f" KCMAX = {args.kappa} \n")
    oo.write(" MAXNLG ="+maxNString)
    oo.write(" MAXNQN ="+maxNString)
    oo.write(f" NELC = {nelectrons}\n")
    oo.write(f" NRANG2 = {args.num}\n")
    oo.write(f" NZ = {Z}\n")
    oo.write(" &END\n")

    oo.close()
    return 0

if not args.file:
    print("No GRASP.INP file specified - assuming GRASP.INP")
    file = 'GRASP.INP'
else:
    file = args.file 

if not (args.kappa):
    args.kappa = 100
    
if not (args.num):
    args.num = 10
    
main(graspinp=file)
