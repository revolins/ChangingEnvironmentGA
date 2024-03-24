import csv
import glob
import re
import pandas
import os
import sys

#csv.field_size_limit(sys.maxsize)
frames = []

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

list_most_common = "Common_Strategy, Condition\n"

#TODO: install tqdm for tracking progress on glob
values_do_not_want = ['pd--1.0_', 'pd-0.3_', 'pd-0.2_', 'pd-0.1_', 'pd-0.0_', 'pd--0.5_', 'pd-0.4_', 'pd-0.5_', 'pd-1.0_', 'pd-7.0_']
for paths in glob.glob("pd_check/*"):
  #print("Start: ", paths)
  if any(filter(lambda x: x in paths, values_do_not_want)):
    continue
  if (os.path.isdir(paths)):
    strategies_df, most_common = make_strategy_dictionary(paths)
    frames.append(strategies_df)
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
    #print("Finished: " + str(paths))
    list_most_common += ",".join(most_common) + "\n"

with open("most_common.csv", "w") as most_common_file:
    for item in list_most_common:
        most_common_file.write(item)

#strategies_df = pandas.concat(frames)
#print("Strategies DF: ", strategies_df)
strategies_df.to_csv("strategies_df.csv", header=False)

# strategies_df = make_strategy_dictionary("pd_check/pd_static_test1_0.0_cost")
# strategies_df.to_csv("most_common.csv", header=False)

