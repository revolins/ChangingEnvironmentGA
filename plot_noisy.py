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

def extract_floats(s):
    pattern = r"[-+]?\d*\.\d+"
    floats = [float(num) for num in re.findall(pattern, s)]
    return floats

def plot_noisy(args):
    list_of_bits = glob.glob(join_path(args.input_folder, '*'))
    #print(list_of_bits)
    summary_df = pd.DataFrame(columns=['Generation', 'group_mean', 'group_sd', 'Condition'])
    for i in list_of_bits:
        assert 'noise' in i, "noise not found in folder name, is noise enabled in test.py?"    
        df = pd.read_csv(i)
        average_values = df.groupby('Generation')[['group_mean', 'group_sd']].sum()
        #average_values.loc[average_values['group_sd'] == 0.0, 'group_sd'] = average_values['group_sd'].mean()
        #average_values.loc[average_values['group_mean'] == np.min(average_values['group_mean']), 'group_mean'] = average_values['group_mean'].mean()
        average_values = average_values[average_values['group_sd'] != 0.0]
        average_values = average_values[average_values['group_mean'] != np.min(average_values['group_mean'])]
        average_values['Condition'] = extract_floats(i)[0]
        average_values = average_values.dropna()
        average_values.reset_index(inplace=True)
        average_values.drop(index=249, inplace=True)
        average_values.reset_index(inplace=True)
        average_values['Generation'] = average_values.index
        #print(average_values)
        summary_df = pd.concat([summary_df, average_values], ignore_index=True)

    conditions = summary_df['Condition'].unique()
    summary_df.to_csv('debug_noise.csv', header=True)
    palette = sns.color_palette("husl", len(conditions))
    print(summary_df)
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=summary_df, x='Generation', y='group_mean', hue='Condition', style='Condition', markers=False, dashes=False, err_style="band", errorbar='ci', palette=palette)
    # ax = plt.gca()
    # for i, condition in enumerate(conditions):
    #     df_condition = summary_df[summary_df['Condition'] == condition]
    #     color = palette[i]
        
    #     ax.fill_between(x=df_condition['Generation'],
    #                     y1=df_condition['group_mean'] - (df_condition['group_sd'] ** 1/5),
    #                     y2=df_condition['group_mean'] + (df_condition['group_sd'] ** 1/5),
    #                     color=color, alpha=0.3)
    plt.title(f'Total Bits of Summary Given Noise Over Time')
    plt.ylabel(f'Total Bits of Summary Given Noise Over Time')
    plt.grid(False)
    plt.savefig('Weighted Average.png')
    #plt.savefig(join_path(args.output_folder, f'Weighted Average_{csv_type[3]}.png'))

def main():
    arg_parser = argparse.ArgumentParser(
        description='Plotting function for handling noisy_data folder.')
    
    # Expects 1 argument: output folder
    arg_parser.add_argument("-i", "--input_folder", type=str, default="noisy_data/highmut")
    args = arg_parser.parse_args()
    plot_noisy(args)
    

if __name__ == "__main__":
    main()