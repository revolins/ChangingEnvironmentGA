import csv
import glob
import re
import pandas
import os
import sys


#Extract all bits_of_memory files to graph them ALL


list_of_bits = glob.glob("/mnt/home/leasmika/ChangingEnvironmentGA/pdoutput2015_June_26size_bit_5/*/bits_of_memory_overtime.csv")

all_bits_df = pandas.DataFrame()

for individual_file in list_of_bits:
  Condition = individual_file.split("/")[-2]
  Condition = Condition.split("_")[3]
  Condition = Condition[3:]
  individual_file_df = pandas.read_csv(individual_file)
  individual_file_df['Condition'] = [Condition] * individual_file_df.shape[0]
  individual_file_df['Generation'] = range(individual_file_df.shape[0])
  all_bits_df = all_bits_df.append(individual_file_df)
  
#print individual_file.split("/")[-2], len(individual_file_df), all_bits_df.shape[0]

#beaker.set('all_bits_df', all_bits_df)
all_bits_df.to_csv("all_bits_df_5_bits.csv", header=False)
