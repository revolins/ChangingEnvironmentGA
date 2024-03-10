"""
This module creates detail files for each generation.
Detail files contain information on each PD org within a generation. 
"""

import csv

# Master function to call all the helpers
def make_file_detail(organisms, past_organisms, current_generation, filepath):
    """
    Create detail file for the current generation. 
    For each organism, include:
    - Length or number of bits of initial (specific) memory 
    - Decision list
    - Initial (specific) memory list
    - Number of orgs alive with the same strategy in the current generation
    - ID
    - Parent ID
    """
    # Print out header for detail file that tells whats in it
    # Print as a csv
    # To print data -- go through all dictionary keys, see strat, print output line: decision list, init memory, bits of mem
    # Contain number of orgs alive with that strat look at cur gen
    # Print out id of orgs
    # Print out id of parents


    # Create csv writer
    filename = filepath + '/detail-' + str(current_generation) + '.csv'
    header = ['Bits' , 'Decisions' , 'Memory' , 'Alive' , 'Id' , 'ParentId']

    # Put data where we want it
    data = []
    
    # Iterate through everything in dictionary
    # You need past_organisms for parents info
    for key in past_organisms:
        row = []
        row.append(key.genotype.number_of_bits_of_memory)
        row.append(key.genotype.decision_list)
        row.append(key.genotype.initial_memory)

        # Number of orgs alive goes here
        number_alive = 0
        for org in organisms:
            if hash(key) == hash(org):
                number_alive += 1
        row.append(number_alive)
        
        row.append([org.id for org in past_organisms[key]])
        row.append([org.parent for org in past_organisms[key]])
        data.append(row)

    # Creates csv file
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


    
    

    
    
