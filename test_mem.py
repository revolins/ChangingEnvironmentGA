import subprocess

for i in range(1,101):
    subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}",  "-c", f"config/pd_config_0.ini", "-o", f"pd_check/pd_static_test{i}_0.0_cost"])
    subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "-c", f"config/pd_config_001.ini", "-o", f"pd_check/pd_static_test{i}_0.01_cost"])
    subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "-c", f"config/pd_config_005.ini", "-o", f"pd_check/pd_static_test{i}_0.05_cost"])
    subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "-c", f"config/pd_config_0075.ini", "-o", f"pd_check/pd_static_test{i}_0.075_cost"])
    subprocess.run(["python", "changing_environment_ga.py", "--seed", f"{i}", "-c", f"config/pd_config_02.ini", "-o", f"pd_check/pd_static_test{i}_0.2_cost"])

subprocess.run(["python", "df_three_all_bits.py"])

subprocess.run(["python", "df_four_bits_of_memory.py"])