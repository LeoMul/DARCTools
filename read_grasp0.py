import numpy as np 

def read_grasp0_inp(file_path):
    
    graspinp = open(file_path,'r')
    orbitals = []

    graspinp_read = graspinp.readlines()
    
    csf_orbs = graspinp_read[1].split()
    num_csfs = int(csf_orbs[0])
    num_orbs = int(csf_orbs[1]) 

    occupations = np.zeros([num_orbs,num_csfs])

    #for ii in range(2,2+num_orbs):
    #    current_line = graspinp_read[ii].split()
#
    #    #print(current_line)
    #    orbitals.append(current_line[0].lower())
    #
    #    if len(current_line) == 2:  
    #        occupations[ii-2,:] = int(current_line[1]) 
    #    else:
    #        for i in range(1,len(current_line)):
    #            occupations[ii-2,i-1] = int(current_line[i])
    for jj in range(0,num_orbs):
        
        line = graspinp_read[jj+2]
        x = line.find('!')
        if x != -1:
            line = line[0:x]

        split_string = line.split()
   
        
        #print(split_string)
        current_orb_string = split_string[0]

        orbitals.append(current_orb_string.lower())
        occupation_string_array = split_string[1:]
        #print(occupation_string_array)
        length_string_array = len(occupation_string_array)

        condensed = check_for_condensed_notation_in_row(occupation_string_array)

        if condensed == False: 
            if length_string_array == 1: 
                occupations[jj,:] = int(occupation_string_array[0])
            elif length_string_array == num_csfs:
                occupations[jj,:] = np.array(occupation_string_array)
            else:
                print("unable to decode this orbital. check orbital no.",jj,current_orb_string)
                import sys 
                sys.exit()
        else:
            try:
                occupations[jj,:] = decode_condensed_notation(occupation_string_array,num_csfs)
            except:
                import sys 
                print("exiting for some reason after trying to read condensed notation - contact lpm ")
                sys.exit()
                print(len(occupation_string_array))
            
    graspinp.close()
    #print(np.shape(occupations))
    return orbitals,occupations


def check_for_condensed_notation_in_row(occupation_string_array):   
    #checks for condensed notatation in grasp input
    for occupation_string in occupation_string_array:
        x = occupation_string.find('*')
        if x != -1:
            return True 
        
    return False

def decode_condensed_notation(occupation_string_array,num_csfs):
    #decodes grasp inp condensed notation
    array = np.zeros(num_csfs)

    offset = 0

    for string in occupation_string_array:
        asterisk_index = string.find('*')

        if asterisk_index == -1:
            array[offset] = int(string)
            offset += 1 
        else:
            num_repeat = int(string[0:asterisk_index])
            repeated_occupation_number = int(string[asterisk_index+1:])
            array[offset:offset+num_repeat] = repeated_occupation_number
            offset = offset + num_repeat
    return array 

def getNuclearCharge(file_path):
    #this is a horrible hack lpm 2.07.25
    import os 
    os.system('grep -B 1 FIX {} > fixdatgrep'.format(file_path))
    f = open('fixdatgrep','r')
    x = f.readline().split()
    f.close()
    os.system('rm fixdatgrep')
    Z = int(x[0])
    
    return Z

#read_grasp0_inp('GRASP.INP')