import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import argparse
import glob
import re
from tqdm import tqdm

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) #For those pesky deprecation warnings

def join_path(output_folder, filename):
        return os.path.join(output_folder, filename)

def extract_integers(s):
    numbers_as_strings = re.findall(r'\d+', s)
    numbers = [int(num) for num in numbers_as_strings]
    return numbers

def plot_noisy(args):
    list_of_bits = glob.glob(join_path(args.input_folder, '*'))
    print(list_of_bits)
    dll_df = pd.DataFrame(columns=['Organism #0', 'Organism #1', 'Organism #2', \
                                   'Organism #3', 'Organism #4', 'Organism #5', \
                                    'Organism #6', 'Organism #7', 'Organism #8', \
                                     'Organism #9', 'Generation', 'Condition', 'Mean'])
    for i in list_of_bits:
        assert 'per' in i, "noise not found in csv name, is noise enabled in test.py?"    
        df = pd.read_csv(i)
        nums = extract_integers(i)
        print(nums)
        organism_columns = [col for col in df.columns if 'Organism' in col]
        df['Mean'] = df.apply(lambda row: np.average(row[:len(organism_columns)]), axis=1)
        df['Condition'] = nums[0]
        dll_df = pd.concat([dll_df, df], ignore_index=True)
    
    summary_df = dll_df.groupby(['Condition', 'Generation'], observed=True).agg(
        group_mean=('Mean', 'mean'),
        group_sd=('Mean', 'std')
    ).reset_index()

    conditions = summary_df['Condition'].unique()
    summary_df.to_csv('debug_noise.csv', header=True)
    palette = sns.color_palette("husl", len(conditions))
    #print(summary_df)
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=summary_df, x='Generation', y='group_mean', hue='Condition', style='Condition', markers=False, dashes=False, err_style="band", errorbar='ci', palette=palette)
    plt.title(f'Aggregated Average Decision List Length per Generation')
    plt.ylabel(f'Decision List Length')
    plt.grid(False)
    plt.savefig('Weighted Average.png')
    #plt.savefig(join_path(args.output_folder, f'Weighted Average_{csv_type[3]}.png'))

def main():
    arg_parser = argparse.ArgumentParser(
        description='Plotting function for handling noisy_data folder.')
    
    # Expects 1 argument: output folder
    arg_parser.add_argument("-i", "--input_folder", type=str, default="noisy_data")
    args = arg_parser.parse_args()
    plot_noisy(args)
    

if __name__ == "__main__":
    main()