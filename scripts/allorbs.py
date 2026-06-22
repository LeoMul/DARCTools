import os 
from grasp import * 
import numpy as np 
nelec = [31,32,33,34,35]

ion_lower = 0 
ion_upper = 4
zzmax = 40 

for ne in nelec:
    pElectrons = ne - 30 
    dd = f'{ne}IsoelectronicSequence'
    try:
        os.mkdir(dd)
    except:
        print('already exists, carryin on')
    os.chdir(dd)
    for zz in range(ne,zzmax+1):
        try:
            os.mkdir('{}'.format(zz))
        except:
            print('already exists')
            #continue
        os.chdir('{}'.format(zz))
#
        numorbs = 1 
        
        check = False 
        
        while not(check):
        
            os.system('grasporbs -k 100 -n {} -f GRASP.INP'.format(numorbs))
            os.system('stg1_orbs &> orbsout')
            os.system("grep 'Recommend Max continuum energy' orbsout > contenergy")
            tt = open('contenergy','r')
            energy = float(tt.readline().split()[-2])
            if energy < 1.8:
                numorbs += 1
            else:
                check = True 
                break
        print(f'Settling on {numorbs} orbs for case {zz}{ne}')

        #os.system('graspstg2')

        
        os.chdir('..')
        
    os.chdir('..')
    
