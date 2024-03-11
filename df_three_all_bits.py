import glob
import pandas

list_of_bits = glob.glob("pd_check/*/bits_of_memory_overtime.csv")
all_bits_df = pandas.DataFrame()

for individual_file in list_of_bits:
  #print("Current File Split (/) : ", str(individual_file.split("/")[-1]))
  Condition = individual_file.split("/")[-1]
  #print("Condition Split (-) : ", str(Condition.split("_")))
  #print("4th Condition Split index : ", str(Condition.split("_")[4]))
  Condition = Condition.split("_")[4]
  #print("Condition : ", str(Condition))
  
  individual_file_df = pandas.read_csv(individual_file)
  individual_file_df['Condition'] = [Condition] * individual_file_df.shape[0]
  individual_file_df['Generation'] = range(individual_file_df.shape[0])
  all_bits_df = all_bits_df._append(individual_file_df)
  
#print individual_file.split("/")[-2], len(individual_file_df), all_bits_df.shape[0]
all_bits_df.to_csv("all_bits_df_static_comp_more_values.csv", header=True)
