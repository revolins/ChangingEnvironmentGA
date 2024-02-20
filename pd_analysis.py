import pd_org

def get_tally_of_number_of_bits_of_memory(organisms):
    """
    Returns a list of length MAX_BITS_OF_MEMORY + 1 where each position represents the number
    of organisms with that many number of bits of memory
    """
     
    bits_of_memory = [org.genotype.number_of_bits_of_memory for org in organisms]
    
    tally = [0 for _ in range(pd_org.MAX_BITS_OF_MEMORY + 1)]
    
    for bits in bits_of_memory:
        tally[bits] += 1
        
    return tally
        
    
    