import subprocess

# Hypothesis 1 - Original Experiment Re-Creation and Correlation Tests
subprocess.run(['python', 'test.py', '--mut_rat', '0.01'])
subprocess.run(['python', 'test.py', '--mut_rat', '0.1'])
subprocess.run(['python', 'test.py', '--static'])

subprocess.run(['python', 'test.py', '--mut_rat', '0.01', '--hybrid'])
subprocess.run(['python', 'test.py', '--mut_rat', '0.1', '--hybrid'])
subprocess.run(['python', 'test.py', '--static', '--hybrid'])

# Hypothesis 2 - Static and No Mutation
subprocess.run(['python', 'test.py', '--static', '--hybrid', '--remove_mem_limit', '--noise', '0.01'])
subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--noise', '0.01'])

subprocess.run(['python', 'test.py', '--static', '--hybrid', '--remove_mem_limit', '--noise', '0.05'])
subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--noise', '0.05'])

subprocess.run(['python', 'test.py', '--static', '--hybrid', '--remove_mem_limit', '--noise', '0.1'])
subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--noise', '0.1'])

subprocess.run(['python', 'test.py', '--static', '--hybrid', '--remove_mem_limit', '--noise', '0.2'])
subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--noise', '0.2'])

subprocess.run(['python', 'test.py', '--static', '--hybrid', '--remove_mem_limit', '--noise', '0.5'])
subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--noise', '0.5'])

subprocess.run(['python', 'test.py', '--static', '--hybrid', '--remove_mem_limit', '--noise', '1.0'])
subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--noise', '1.0'])

##### Hypothesis 2 - Low Mutation
subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.01'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.05'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.1'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.2'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.5'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '1.0'])
##### Hypothesis 2 - High Mutation
subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.1', '--noise', '0.01'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.1', '--noise', '0.05'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.1', '--noise', '0.1'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.1', '--noise', '0.2'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.1', '--noise', '0.5'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.1', '--noise', '1.0'])

##### Hypothesis 3 - Friendly
subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.01', '--env_seed', 'coop'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.05', '--env_seed', 'coop'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.1', '--env_seed', 'coop'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.2', '--env_seed', 'coop'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.5', '--env_seed', 'coop'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '1.0', '--env_seed', 'coop'])

##### Hypothesis 3 - Hostile
subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.01', '--env_seed', 'hostile'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.05', '--env_seed', 'hostile'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.1', '--env_seed', 'hostile'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.2', '--env_seed', 'hostile'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '0.5', '--env_seed', 'hostile'])

subprocess.run(['python', 'test.py', '--hybrid', "--remove_mem_limit", '--mut_rat', '0.01', '--noise', '1.0', '--env_seed', 'hostile'])

subprocess.run(['python', 'plot_decision.py', '--et', 'coop'])

subprocess.run(['python', 'plot_decision.py', '--et', 'hostile'])

subprocess.run(['python', 'plot_decision.py', '--et', 'maxmemlowmut'])