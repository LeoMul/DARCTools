import os 
#from grasp import * 
#import numpy as np 
nelec = [31,32,33,34,35]

#nelec = [33]

zzmax = 40

ion_lower = 0 
ion_upper = 4

core = [ 2, 2, 6, 2, 6,10]
orbs = ['1S','2S','2P','3S','3P','3D','4S','4P','5S']

for ne in nelec:
    pElectrons = ne - 30  
    dd = f'{ne}IsoelectronicSequence'
    for zz in range(ne,zzmax+1):
        os.system(f'cp {dd}/{zz}/adf04_ups /lustre/dirac3/scratch/dp375/dc-mulh1/FirstPeak/smallCalc/quickADF/adf04{zz}{ne}')
