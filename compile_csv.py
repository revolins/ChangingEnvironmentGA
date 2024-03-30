import csv
import glob
import re
import pandas
import os
import argparse

def join_path(output_folder, filename):
        return os.path.join(output_folder, filename)

def build_experiment_csv(output_folder):
    list_of_bits = glob.glob(join_path(output_folder, '*/bits_of_memory_overtime.csv'))
    all_bits_df = pandas.DataFrame()

    print("Compiling Experimental Memory Results")
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
    all_bits_df.to_csv(join_path(output_folder, 'all_bits_df_static_comp_more_values.csv'), header=True)

def make_strategy_dictionary(fileregx):
  def atoi(text):
      return int(text) if text.isdigit() else text

  def natural_keys(text):
      '''
      alist.sort(key=natural_keys) sorts in human order
      http://nedbatchelder.com/blog/200712/human_sorting.html
      (See Toothy's implementation in the comments)
      '''
      return [ atoi(c) for c in re.split('(\d+)', text) ]


  filelist = glob.glob(fileregx + "/detail-*.csv")

  number_of_strategies = {}

  filelist.sort(key=natural_keys)
  #initializing dictionary
  #puts all the strategies ever into dictionary
  last_file = filelist[-1]

  with open(last_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
      if row == []:
        continue
      key = row[1] + "~" + row[2]
      number_of_strategies[key] = []

  #makes keys of decisionlist+memory
  #adds number of alive to the keys location in dictionary

  for individual_file in filelist:
    with open(individual_file, 'r') as csvfile:
      reader = csv.reader(csvfile)
      next(reader)
      for row in reader:
        if row == []:
          continue
        key = row[1] + "~" + row[2]
        number_of_strategies[key].append(int(row[3]))
    max_list_length = max([ len(number_of_strategies[l]) for l in number_of_strategies])
    for key in number_of_strategies:
      if len(number_of_strategies[key]) < max_list_length:
        number_of_strategies[key].append(0)
   
  #picking out bad strats and makes a list of them
  failed_strategies = []
  for key in number_of_strategies:
    if sum(number_of_strategies[key]) <= 1:
      failed_strategies.append(key)

  #this is creating list of best common strategy
  common_one_strategy = [ (number_of_strategies[key][-1], key) for key in number_of_strategies]
  common_one_strategy = max(common_one_strategy, key= lambda x: x[0])[1]

  #delete bad strats from main dictionary
  for key in failed_strategies:
    del(number_of_strategies[key])

  strategies_df = pandas.DataFrame.from_dict(number_of_strategies, orient= 'index')
  #concatenating multiple data frames
  Condition = fileregx.split("/")[-1]
  Condition = Condition.split("_")[4]
  Condition = Condition[3:]
  strategies_df['Condition'] = [Condition] * len(number_of_strategies)
  strategies_df['Strategy'] = number_of_strategies.keys()
  
  return strategies_df, [common_one_strategy, Condition]

def format_common_strat(most_common):
    most_common[0] = most_common[0].split("~")
    most_common[0] = [eval(strat) for strat in most_common[0]]
    binary_most_common = ""
    for ls in most_common[0]:
      for bit in ls:
        if bit:
          binary_most_common += str(1)
        else:
          binary_most_common += str(0)
      binary_most_common += "~"
    most_common[0] = binary_most_common

    return most_common

def build_strat_csv(output_folder):
    frames = []
    list_most_common = "Common_Strategy, Condition\n"

    values_do_not_want = ['pd--1.0_', 'pd-0.3_', 'pd-0.2_', \
                           'pd-0.1_', 'pd-0.0_', 'pd--0.5_', \
                            'pd-0.4_', 'pd-0.5_', 'pd-1.0_', \
                                  'pd-7.0_']
    
    print("Compiling Strategy Results")
    for paths in glob.glob(join_path(output_folder, "*")):
        #print("Start: ", paths)
        if any(filter(lambda x: x in paths, values_do_not_want)):
            continue
        if (os.path.isdir(paths)):
            strategies_df, most_common = make_strategy_dictionary(paths)
            frames.append(strategies_df)
            most_common = format_common_strat(most_common)
            #print("Finished: " + str(paths))
            list_most_common += ",".join(most_common) + "\n"

    with open(join_path(output_folder, "most_common.csv"), "w") as most_common_file:
        for item in list_most_common:
            most_common_file.write(item)

    #strategies_df = pandas.concat(frames)
    #print("Strategies DF: ", strategies_df)
    strategies_df.to_csv(join_path(output_folder, "strategies_df.csv"), header=False)

def main():
    arg_parser = argparse.ArgumentParser(
        description='Plotting function for compiled csvs.')
    
    # Expects 1 argument: output folder
    arg_parser.add_argument("-o", "--output_folder", type=str, default="tests/pd_temp")
    args = arg_parser.parse_args()

    build_experiment_csv(args.output_folder)
    build_strat_csv(args.output_folder)
    

if __name__ == "__main__":
    main()