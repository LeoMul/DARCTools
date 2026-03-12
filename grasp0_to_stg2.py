import read_grasp0
import stg2_lib
import numpy as np 
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file',  help='Specify path of GRASP.INP file')
parser.add_argument('-l','--num_levels',  help='Number of close-coupling levels',type= int)
parser.add_argument('-p', '--num_partial_waves',  help='Number of N+1 partial waves',type=int)
parser.add_argument('-c', '--ncorinc',  help='Value of ncorinc',type=int)
parser.add_argument('-a', '--all',  help='Print 3 files for autoruns',action='store_true')

args = parser.parse_args()

def main(num_partial_waves,num_levels_cc,graspinp):
    nr_peel,occupations = read_grasp0.read_grasp0_inp(graspinp)
    
    funcArgs = [num_levels_cc,
                num_partial_waves,
                [],
                nr_peel,
                np.transpose(occupations),
                args.ncorinc]
    
    if args.all:
        stg2_lib.write_dstg2(*funcArgs,dim=0,ang=-1,file='DSTG2.INP1')
        stg2_lib.write_dstg2(*funcArgs,dim=1,ang= 0,file='DSTG2.INP2')
        stg2_lib.write_dstg2(*funcArgs,dim=1,ang= 1,file='DSTG2.INP3')
    else:
    
        stg2_lib.write_dstg2(*funcArgs)

    return 0

if not args.file:
    print("No GRASP.INP file specified - assuming GRASP.INP")
    file = 'GRASP.INP'
else:
    file = args.file 

if not args.num_partial_waves:
    print("no partial waves requested")
    parser.print_help()
    exit()

if not args.num_levels:
    print("no cc levels requested")
    parser.print_help()
    exit()

main(num_partial_waves=args.num_partial_waves,
     num_levels_cc=args.num_levels,
     graspinp=file)
