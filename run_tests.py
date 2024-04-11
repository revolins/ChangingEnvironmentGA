import subprocess

# Simple script for running tests locally -- update with your desired commands
# If you have the compute power, you can run multiple prompt windows with different tests
# Since it's so simple I just make a copy of this file and then update the commands that are run
subprocess.run(['python', 'test.py', '--mut_rat', '0.01', '--nt', '1000', '--ignore_matching'])
subprocess.run(['python', 'test.py', '--mut_rat', '0.1', '--nt', '1000', '--ignore_matching'])
subprocess.run(['python', 'test.py', '--static', '--nt', '1000', '--ignore_matching'])