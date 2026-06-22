import os 
from grasp import * 
import numpy as np 
nelec = [31,32,33,34,35]

nelec = [33]

zzmax = 40

ion_lower = 0 
ion_upper = 4

core = [ 2, 2, 6, 2, 6,10]
orbs = ['1S','2S','2P','3S','3P','3D','4S','4P','5S']

for ne in nelec:
    pElectrons = ne - 30 
    dd = f'{ne}IsoelectronicSequence'
    try:
        os.mkdir(dd)
    except:
        print('already exists, carryin on')
    os.chdir(dd)
    
    
    baseConfig = [2,pElectrons,0]
    maxes      = [2,6,2]
    configs = [baseConfig]

    configs.append([2,pElectrons-1,1])

    if pElectrons + 1 <=6:
        configs.append([1,pElectrons+1,0])
        
    if pElectrons + 2 <=6:
        configs.append([0,pElectrons+2,0])
        
    configs.append([1,pElectrons,1])

    configs = np.array(configs)
    graspInput(configs)
    print(configs)
#    for zz in range(ne,zzmax+1):
    #for zz in range(38,39):
    for zz in range(ne,zzmax+1):
        try:
            os.mkdir('{}'.format(zz))
        except:
            print('already exists')
            #continue
        os.chdir('{}'.format(zz))
        
        graspInput(configs,zz,1,False)
        os.system('grasp0 &> output')
        os.system('tail -n 1 output > check')
        os.system('grasp_ls -f GRASP.OUT -u 2 > ls.dat.run1')
        os.system('mv GRASP.OUT GRASP.STRUC')

        ee =  open('check','r')
        tt = ee.readline()
        if not ('normally' in tt):
            import sys
            print('failure in run 1, zz = ',zz) 
            sys.exit()
        else:
            print('Success in run 1, zz= ',zz,'ne=',ne)
        ff = open('inp','w')
        ff.write('1')
        ff.close()
        os.system('/lustre/dirac3/scratch/dp375/dc-mulh1/FirstPeak/grasp/stg1d0_i8.x < inp &>stg1d0Out')
    
        ee.close()
        #os.system(f'cp ../{zz}{ne}.shift shift')
        
        ss = np.loadtxt(f'../{zz}{ne}.shift')
        shiftFile = open('shift','w')
        for s in ss:
            shiftFile.write(f'{s/109737.316}\n')
        shiftFile.close()
        
        graspInput(configs,zz,1,True)
        os.system('grasp0 &> output')
        os.system('mv GRASP.OUT GRASP.OUT1')
        graspInput(configs,zz,2,True)
        os.system('grasp0 &> output')
        os.system('mv GRASP.OUT GRASP.OUT2')
        graspInput(configs,zz,3,True)
        os.system('grasp0 &> output')
        os.system('mv GRASP.OUT GRASP.OUT3')
        os.system('mv GRASP.STRUC GRASP.OUT')

        os.system('avalue -d GRASP.OUT1 GRASP.OUT2 GRASP.OUT3 -e shift > avalueOut')
        
        os.chdir('..')
        
    os.chdir('..')
