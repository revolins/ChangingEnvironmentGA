import random

decision_list = [1, 2, 1, 2, 1, 1]  # Example decision_list
old_memory_bits = 1 # (k)
old_summary_bits = 2 # (j)
assert(len(decision_list) == 2 ** old_memory_bits * (old_summary_bits + 1))

new_memory_bits = old_memory_bits + 1 # (k)
new_summary_bits = old_summary_bits + 1 # (j)

len_new_dec_list = int(2 * len(decision_list) * ((new_summary_bits + 1) / (old_summary_bits + 1)))
print(len_new_dec_list) # this and
print(2 ** new_memory_bits * (new_summary_bits + 1)) # this should be the same (2^k*(j+1))

# new_dec_list = 2 * decision_list * ((new_summary_bits + 1) // (old_summary_bits + 1))

# print(new_dec_list)
# print (len(new_dec_list))

new_dec_list = 2 * decision_list
print(new_dec_list) # print doubled list

for i in range(len_new_dec_list - len(new_dec_list)):
    new_dec_list.append(random.choice(decision_list))
print(new_dec_list) # print final list
print(len(new_dec_list)) # this should alos be the same as the ones above