import csv
import glob
import re
import pandas
import os
import sys


#Extract all bits_of_memory files to graph them ALL
#Looks like they follow a folder structure thats dependent on the memory condition
#So three nest subfolders?? before they reach the condition necessary for the Kruskal plot

list_of_bits = glob.glob("pd_check/*/bits_of_memory_overtime.csv")

all_bits_df = pandas.DataFrame()

for individual_file in list_of_bits:
  print(individual_file.split("/")[-1])
  Condition = individual_file.split("/")[-1]
  print(Condition.split("_"))
  print(Condition.split("_")[4])
  Condition = Condition.split("_")[4]
  Condition = Condition[3:]
  
  individual_file_df = pandas.read_csv(individual_file)
  individual_file_df['Condition'] = [Condition] * individual_file_df.shape[0]
  individual_file_df['Generation'] = range(individual_file_df.shape[0])
  all_bits_df = all_bits_df._append(individual_file_df)
  
#print individual_file.split("/")[-2], len(individual_file_df), all_bits_df.shape[0]

#beaker.set('all_bits_df', all_bits_df)
all_bits_df.to_csv("all_bits_df_static_comp_more_values.csv", header=True)
