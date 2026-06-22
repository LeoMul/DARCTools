import os 

#todo - make use of restart.in principle not hard.

def Configs(ne):
    numcf = 0
    cfList = []

    match ne:
        case 31:
            numcf = 6 
            cfList = ['2 1 0',
                      '1 2 0',
                      '0 3 0',
                      '2 0 1',
                      '1 1 1',
                      '0 2 1']
        case 32:
            numcf = 6
            cfList = ['2 2 0',
                      '1 3 0',
                      '0 4 0',
                      '2 1 1',
                      '1 2 1',
                      '0 3 1']
        case 33:
            numcf = 6
            cfList = ['2 3 0',
                      '1 4 0',
                      '0 5 0',
                      '2 2 1',
                      '1 3 1',
                      '0 4 1']
        case 34:
            numcf = 6
            cfList = ['2 4 0',
                      '1 5 0',
                      '0 6 0',
                      '2 3 1',
                      '1 4 1',
                      '0 5 1']
        case 35:
            numcf =5 
            cfList = ['2 5 0',
                      '1 6 0',
                      '2 4 1',
                      '1 5 1',
                      '0 6 1']
        case 36:
            numcf =3
            cfList = ['2 6 0',
                      '2 5 1',
                      '1 6 1']
            
        case _:
            print(f'{ne} not able to be matched - aborting?')
            import sys 
            sys.exit()
            return -1,[]
    
    return numcf, cfList 


def struc(zz,ne):
    
    numcf_nelec, cflist_nelec = Configs(ne)
    
    ff = open('das','w')
    ff.write("A.S.\n")
    ff.write(f"&SALGEB CUP='ICR' MXVORB= 3 MXCONF=  {numcf_nelec} KUTSS=-1 KUTSO= 0 KUTOO= 0 korb1=1 korb2=6 &END\n")
    ff.write("  4  0  4  1 4  2\n")
    
    for ii in range(0,numcf_nelec):
        ff.write( cflist_nelec[ii] + '\n')
        
    ff.write(f"&SMINIM NZION= {zz}  INCLUD=10 &END \n")
    ff.write("&SRADCON EMIN=0 EMAX=2 MENG=-15 &END\n")
    ff.write("&DRR NMIN=5 NMAX=5 LMIN=0 LMAX=0 &END\n")
    ff.close()
    return 0

def DR(zz,lam,ne,restart=0,restartpath=''):
    
    numcf_nelec,   cflist_nelec   = Configs(ne)
    numcf_nelecP1, cflist_nelecP1 = Configs(ne+1)
    print(numcf_nelecP1)
    ff = open('das','w')
    ff.write('A.S.\n')
    os.system('rm RESTART')
    if (restart != 1 and restart != 0):
        os.system(f'ln -s {restartpath} RESTART')
    
    ff.write(f"&SALGEB RUN='DR' MXCCF={numcf_nelecP1} CUP='ICR' MXVORB= 3 MXCONF=  {numcf_nelec} KUTSS=-1 KUTSO= 0 KUTOO= 0 korb1=1 korb2=6 MSTART={
restart} &END\n")
    
    
    ff.write("  4  0  4  1 4  2 \n")
    for ii in range(0,numcf_nelec):
        ff.write( cflist_nelec[ii] + '\n')
    for ii in range(0,numcf_nelecP1):
        ff.write( cflist_nelecP1[ii] + '\n')
        
    ff.write(f"&SMINIM NZION= {zz}  nlam=9 PRINT='UNFORM' &END\n") 
    string = len(lam)*' {}'
    string += '\n'
    ff.write(string.format(*lam))
    ff.write('&DRR NMIN=5 NMAX=50 LMIN=0 LMAX=9 &END\n')
    ff.write('&SRADCON EMIN=0 EMAX=2 MENG=-15 &END\n')
    ff.close()
    return 0

def RR(zz,lam,ne,restart=0,restartpath=''):
    numcf_nelec,   cflist_nelec   = Configs(ne)
    numcf_nelecP1, cflist_nelecP1 = Configs(ne+1)
    if (restart != 1 and restart!=0):
        os.system('rm RESTART')
        os.system(f'ln -s {restartpath} RESTART')
        
    ff = open('das','w')
    ff.write('A.S.\n')
    ff.write(f"&SALGEB RUN='RR' MXCCF={numcf_nelecP1} CUP='ICR' MXVORB= 3 MXCONF=  {numcf_nelec} KUTSS=-1 KUTSO= 0 KUTOO= 0 korb1=1 korb2=6 LCON=7 M
START={restart} &END\n")
    ff.write("  4  0  4  1 4  2 \n")
    for ii in range(0,numcf_nelec):
        ff.write( cflist_nelec[ii] + '\n')
    for ii in range(0,numcf_nelecP1):
        ff.write( cflist_nelecP1[ii] + '\n')
    ff.write(f"&SMINIM NZION= {zz}  nlam=9 PRINT='UNFORM' &END\n") 
    string = len(lam)*' {}'
    string += '\n'
    ff.write(string.format(*lam))
    ff.write('&DRR NMIN=5 NMAX=30 LMIN=0 LMAX=5 LCON=7 &END\n')
    ff.write('&SRADCON MENG=21 &END\n') 
    ff.write(' 0.00000E+00    8.16334E-02    1.69931E-01    2.65436E-01    3.68738E-01    4.80473E-01    6.01329E-01    7.32051E-01 8.73444E-01    1
.02638E+00    1.19180E+00    1.37072E+00    1.56425E+00    1.77358E+00    2.00000E+00    2.10000E+00 4.60000E+00    1.00000E+01    2.10000E+01    4.
60000E+01    1.00000E+02')
    ff.close()
    return 0

def PICore(zz,lam,ne,restart=0,restartpath=''):
    numcf_nelec,   cflist_nelec   = Configs(ne)
    numcf_nelecP1, cflist_nelecP1 = Configs(ne+1)    
    if (restart != 1 and restart!=0):
        os.system('rm RESTART')
        os.system(f'ln -s {restartpath} RESTART')
    ff = open('das','w')
    ff.write('A.S.\n')
    ff.write(f"&SALGEB RUN='PI' MXCCF={numcf_nelecP1} CUP='ICR' MXVORB= 3 MXCONF=  {numcf_nelec} KUTSS=-1 KUTSO= 0 KUTOO= 0 korb1=1 korb2=6 LCON=7 M
START={restart} &END\n")
    ff.write("  4  0  4  1 4  2 \n")
    for ii in range(0,numcf_nelec):
        ff.write( cflist_nelec[ii] + '\n')
    for ii in range(0,numcf_nelecP1):
        ff.write( cflist_nelecP1[ii] + '\n')
    ff.write(f"&SMINIM NZION= {zz}  nlam=9 PRINT='UNFORM' &END\n") 
    string = len(lam)*' {}'
    string += '\n'
    ff.write(string.format(*lam))
    ff.write('&SRADCON MENG=21 &END\n') 
    ff.write(' 0.00000E+00    8.16334E-02    1.69931E-01    2.65436E-01    3.68738E-01    4.80473E-01    6.01329E-01    7.32051E-01 8.73444E-01    1
.02638E+00    1.19180E+00    1.37072E+00    1.56425E+00    1.77358E+00    2.00000E+00    2.10000E+00 4.60000E+00    1.00000E+01    2.10000E+01    4.
60000E+01    1.00000E+02')
    ff.close()
    return 0

def getLambdaParameters():
    lambdaParams = []
    os.system('grep -A 2 "SCALING" olg > scalingParameters.dat ')
    tt = open('scalingParameters.dat')
    line = tt.readline().split()[-5:]
    for t in line:
        lambdaParams.append(t)
    line = tt.readline().split()
    for t in line:
        lambdaParams.append(t)
        
    tt.close()
    
    return lambdaParams 

def adasin(dr=True):
    temps = [1.00E+01,
             2.00E+01,
             5.00E+01,
             1.00E+02,
             2.00E+02,
             5.00E+02,
             1.00E+03,
             2.00E+03,
             5.00E+03,
             1.00E+04,
             2.00E+04,
             5.00E+04,
             1.00E+05,
             2.00E+05,
             5.00E+05,
             1.00E+06,
             2.00E+06,
             5.00E+06,
             1.00E+07]
    tt = open('temps','w')
    for t in temps:
        tt.write(f'{t}\n')
    tt.close()
    os.system('wc ../struc/LEVELS > numlevels')
    numlevfile = open('numlevels','r')
    length = int(numlevfile.readline().split()[0]) - 2
    numlevfile.close()
    
    ff = open('adasinStart','w')
    ff.write("/IC/ \n")
    if dr:
        ff.write(f"&ONE NTAR1=1 NTAR2={length} COREX=' - '  &END\n")
        ff.write("&TWO jtemp=19 NRB=-1 &END\n")
    else:
        ff.write(f"&ONE NTAR1=1 NTAR2=0   &END\n")
        ff.write("&TWO jtemp=19 &END\n")

        
    
    ff.close()
    os.system('tail -n +2 ../struc/LEVELS > levels')
    os.system('cat adasinStart levels temps > adasin')

    return 0

def performStructureRun(zz,ne,run = False):
    try:
        os.mkdir('struc')
    except:
        print('contnue')
    os.chdir('struc')
    struc(zz,ne)
    if run:
        os.system('auto_lap < das')
    ll = getLambdaParameters()
    print(ll)
    os.chdir('..')
    return ll

def performDRRun(ll,ne,run=False,restart=0,restartpath=''):
    try:
        os.mkdir('dr')
    except:
        print('contnue')
    os.chdir('dr')
    DR(zz,ll,ne,restart,restartpath)
    if run:
        print('attempting DR run')
        os.system('auto_lap < das')
    else:
        print('skipping this run...')
    adasin()
    os.system('ln -s oicu o1u')
    
    os.system('/mnt/scratch2/users/40268323/FirstPeakDR/adasdr.x < adasin ')
    os.system('grep -A 20 "T(K)" adf09 > dr.dat')
    os.chdir('..')
    
    return 0

def performRRrun(ll,ne,run=False,restart=0,restartpath=''):
    try:
        os.mkdir('rr')
    except:
        print('contnue')
    os.chdir('rr')
    RR(zz,ll,ne,restart,restartpath)
    if run:
        os.system('auto_lap < das')
    adasin(dr=False)
    os.system('ln -s opicu op1u')
    os.system('ln -s oicu o1u')

    #if run:
    #    os.system('~/adasdr/adasrr.x < adasin')
    #os.system('grep -A 20 "T(K)" adf09 > dr.dat')
    os.chdir('..')
    return 0 

def performPIrun(ll,ne,run=False,restart=0,restartpath=''):
    try:
        os.mkdir('pi')
    except:
        print('contnue')
    os.chdir('pi')
    PICore(zz,ll,ne,restart,restartpath)
    if run:
        os.system('auto_lap < das')
    adasin(dr=False)
    
    os.system('rm op1u o1u op2u o2u')
    
    os.system('ln -s opicu op1u')
    os.system('ln -s oicu o1u')
    os.system('ln -s ../rr/opicu op2u')
    os.system('ln -s ../rr/oicu o2u')

    
    os.system('/mnt/scratch2/users/40268323/FirstPeakDR/adasrr.x < adasin')
    os.system('grep -A 20 "T(K)" adasout > dr.dat')
    os.chdir('..')
    return 0 


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--inputs', nargs='+', type=int, help='A list of integers = number of target electrons')
parser.add_argument('--start', type=int, help='Sets starting z. First z calculated = ne+1+start.')
args = parser.parse_args()

print(f"Your list: {args.inputs}")



if not args.inputs:
    import sys 
    nelist = range(31,37)
    print('using default range! beware of the long runtime.')
else:
    nelist = args.inputs    



for ne in nelist:
    
    
    try:
        os.mkdir(f'{ne}Isoelectronic')
    except:
        print(f'{ne}Isoelectronic exists.')
    
    os.chdir(f'{ne}Isoelectronic')
    
    restart = 1 
    restartpathdr =''
    restartpathrr =''
    restartpathpi =''
    start = 0
    if args.start:
        start = int(args.start)
    print('starting at ne+1+start')

    for zz in range(ne+1+start,40):
        try:
            os.mkdir(f'{zz}')
        except:
            print('contuning')
        os.chdir(f'{zz}')

        ll = performStructureRun(zz,ne,run=True)
        
        #os.system('rm ls.dat; cd struc ; as_ls -l oic > ls.dat')
        if (zz>ne+1):
            restart = 5 
            restartpathdr = f'/mnt/scratch2/users/40268323/FirstPeakDR/{ne}Isoelectronic/{ne+1}/dr/RESTART'
            restartpathrr = f'/mnt/scratch2/users/40268323/FirstPeakDR/{ne}Isoelectronic/{ne+1}/rr/RESTART'
            restartpathpi = f'/mnt/scratch2/users/40268323/FirstPeakDR/{ne}Isoelectronic/{ne+1}/pi/RESTART'

        performDRRun(ll,ne,run=True,restart=restart,restartpath=restartpathdr)
        performRRrun(ll,ne,run=True,restart=restart,restartpath=restartpathrr)
        performPIrun(ll,ne,run=True,restart=restart,restartpath=restartpathpi)
        #
        os.chdir('..')
    #
    os.chdir('..')
