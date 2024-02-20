"""
Detail file for pd_organisms
"""

import csv

#master function to call all the helpers
def make_file_detail(organisms, past_organisms, current_generation, filepath):
    # print out header for detail file that tells whats in it
    # print as a csv
    # to print data -- go through all dictionary keys, see strat, print output line: decision list, init memory, bits of mem
    # contain number of orgs alive with that strat look at cur gen
    # print out id of orgs
    # printo out id of parents


    # create csv writer
    filename = filepath + '/detail-' + str(current_generation) + '.csv'
    header = ['Bits' , 'Decisions' , 'Memory' , 'Alive' , 'Id' , 'ParentId']

    # put data where we want it
    data = []
    
    # iterate through everything in dictionary
    for key in past_organisms:
        row = []
        row.append(key.genotype.number_of_bits_of_memory)
        row.append(key.genotype.decision_list)
        row.append(key.genotype.initial_memory)
        # number of orgs alive goes here
        number_alive = 0
        for org in organisms:
            if hash(key) == hash(org):
                number_alive += 1
        row.append(number_alive)
        row.append([org.id for org in past_organisms[key]])
        row.append([org.parent for org in past_organisms[key]])
        data.append(row)
    # creates csv file
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


    
    

    
    
