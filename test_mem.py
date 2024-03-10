import subprocess

for i in range(1,6):
    subprocess.run(["python", "changing_environment_ga.py", "-c", f"config/pd_config_0.ini", "-o", f"pd_check/pd_static_test{i}_0.0_cost"])
    subprocess.run(["python", "changing_environment_ga.py", "-c", f"config/pd_config_01.ini", "-o", f"pd_check/pd_static_test{i}_0.1_cost"])
    subprocess.run(["python", "changing_environment_ga.py", "-c", f"config/pd_config_001.ini", "-o", f"pd_check/pd_static_test{i}_0.01_cost"])
    subprocess.run(["python", "changing_environment_ga.py", "-c", f"config/pd_config_05.ini", "-o", f"pd_check/pd_static_test{i}_0.5_cost"])

subprocess.run(["python", "pd_beaker_three_all_bits_df.py"])

subprocess.run(["python", "pd_beaker_four_bits_of_memory_df.py"])