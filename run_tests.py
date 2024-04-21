import subprocess

# Hypothesis 1
# subprocess.run(['python', 'test.py', '--mut_rat', '0.01'])
# subprocess.run(['python', 'test.py', '--mut_rat', '0.1'])
# subprocess.run(['python', 'test.py', '--static'])

# subprocess.run(['python', 'test.py', '--mut_rat', '0.01', '--hybrid'])
# subprocess.run(['python', 'test.py', '--mut_rat', '0.1', '--hybrid'])
# subprocess.run(['python', 'test.py', '--static', '--hybrid'])

# # Hypothesis 2
# subprocess.run(['python', 'test.py', '--static', '--hybrid', '--remove_mem_limit', '--noise', '0.01'])
# subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--noise', '0.01'])

# subprocess.run(['python', 'test.py', '--static', '--hybrid', '--remove_mem_limit', '--noise', '0.05'])
# subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--noise', '0.05'])

# subprocess.run(['python', 'test.py', '--static', '--hybrid', '--remove_mem_limit', '--noise', '0.1'])
# subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--noise', '0.1'])

# subprocess.run(['python', 'test.py', '--static', '--hybrid', '--remove_mem_limit', '--noise', '0.2'])
# subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--noise', '0.2'])

# subprocess.run(['python', 'test.py', '--static', '--hybrid', '--remove_mem_limit', '--noise', '0.5'])
# subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--noise', '0.5'])

# subprocess.run(['python', 'test.py', '--static', '--hybrid', '--remove_mem_limit', '--noise', '1.0'])
# subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--noise', '1.0'])

# #####
subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.01'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.05'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.1'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.2'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.5'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '1.0'])
# #####
subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.1', '--noise', '0.01'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.1', '--noise', '0.05'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.1', '--noise', '0.1'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.1', '--noise', '0.2'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.1', '--noise', '0.5'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.1', '--noise', '1.0'])