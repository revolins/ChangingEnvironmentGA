import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import argparse

from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison
from statsmodels.tsa.stattools import grangercausalitytests
from tqdm import tqdm

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) #For those pesky deprecation warnings

def join_path(output_folder, filename):
        return os.path.join(output_folder, filename)

def retrieve_dll(args):
    print(f"Retrieving Decision List Length Plots")
    bits_of_memory_df = pd.read_csv(join_path(args.output_folder, f"decision_list_length_overtime.csv"))
    bits_of_memory_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    read_columns = bits_of_memory_df.columns[1:-2]
    bits_of_memory_df.drop(bits_of_memory_df.columns[0], axis=1, inplace=True)
    bits_of_memory_df['Generation'] = pd.to_numeric(bits_of_memory_df['Generation'], errors='coerce')
    bits_of_memory_df['Condition'] = pd.Categorical(pd.to_numeric(bits_of_memory_df['Condition'], errors='coerce'))
    for col in tqdm(read_columns):
        bits_of_memory_df[col] = pd.to_numeric(bits_of_memory_df[col], errors='coerce')

    # weights = np.arange(1, len(read_columns) + 1)
    # weights = weights / weights.sum()
    bits_of_memory_df['Mean'] = bits_of_memory_df.apply(lambda row: np.average(row[:len(read_columns)]), axis=1)

    summary_df = bits_of_memory_df.groupby(['Condition', 'Generation'], observed=True).agg(
        group_mean=('Mean', 'mean'),
        group_sd=('Mean', 'std')
    ).reset_index()

    return summary_df, bits_of_memory_df, read_columns

def average_dll(args):
    
    summary_df, bits_of_memory_df, read_columns = retrieve_dll(args)
    conditions = summary_df['Condition'].unique()

    palette = sns.color_palette("husl", len(conditions))
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=summary_df, x='Generation', y='group_mean', hue='Condition', style='Condition', markers=False, dashes=False, err_style="band", errorbar='ci', palette=palette)
    ax = plt.gca()
    for i, condition in enumerate(conditions):
        df_condition = summary_df[summary_df['Condition'] == condition]
        color = palette[i]
        
        ax.fill_between(x=df_condition['Generation'],
                        y1=df_condition['group_mean'] - (df_condition['group_sd'] ** 1/len(read_columns)),
                        y2=df_condition['group_mean'] + (df_condition['group_sd'] ** 1/len(read_columns)),
                        color=color, alpha=0.3)
    plt.title(f'Average Decision List Length Over Time')
    plt.ylabel(f'Average Decision List Length')
    plt.grid(False)
    plt.savefig(join_path(args.output_folder, f'Average_Decision_List_Length.png'))

    palette = sns.color_palette("husl", len(conditions))
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=summary_df, x='Generation', y='group_mean', hue='Condition', style='Condition', markers=False, dashes=False, palette=palette)
    plt.title(f'Average Decision List Length Over Time')
    plt.ylabel(f'Average Decision List Length')
    plt.grid(False)
    plt.savefig(join_path(args.output_folder, f'Average_Decision_List_Length_NoDashes.png'))

    plt.figure(figsize=(10, 6))
    plt.hist(bits_of_memory_df['Mean'], bins=30)
    plt.title(f'Distribution of Mean Decision List Length')
    plt.xlabel(f'Mean Decision List Length')
    plt.ylabel('Frequency')
    plt.savefig(join_path(args.output_folder, f'Mean_Decision_List_Length.png'))

def average_mem(args, csv):
    csv_type = csv.split('_')
    print(f"Constructing {csv_type[3].upper()} Plots and Running Statistical Tests")
    bits_of_memory_df = pd.read_csv(join_path(args.output_folder, f"all_bits_df_{csv_type[3]}_comp_more_values.csv"))
    bits_of_memory_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    read_columns = bits_of_memory_df.columns[1:-2]
    bits_of_memory_df.drop(bits_of_memory_df.columns[0], axis=1, inplace=True)
    bits_of_memory_df['Generation'] = pd.to_numeric(bits_of_memory_df['Generation'], errors='coerce')
    bits_of_memory_df['Condition'] = pd.Categorical(pd.to_numeric(bits_of_memory_df['Condition'], errors='coerce'))
    for col in tqdm(read_columns):
        bits_of_memory_df[col] = pd.to_numeric(bits_of_memory_df[col], errors='coerce')

    weights = np.arange(1, len(read_columns) + 1)
    weights = weights / weights.sum()
    bits_of_memory_df['Mean'] = bits_of_memory_df.apply(lambda row: np.average(row[:len(read_columns)], weights=weights), axis=1)

    dll_df, _, _ = retrieve_dll(args)
    summary_df = bits_of_memory_df.groupby(['Condition', 'Generation'], observed=True).agg(
        group_mean=('Mean', 'mean'),
        group_sd=('Mean', 'std')
    ).reset_index()

    if 'noise' in args.output_folder:
        summary_df.to_csv(f'noisy_data/{args.output_folder}_summary.csv')

    conditions = summary_df['Condition'].unique()

    palette = sns.color_palette("husl", len(conditions))
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=summary_df, x='Generation', y='group_mean', hue='Condition', style='Condition', markers=False, dashes=False, err_style="band", errorbar='ci', palette=palette)
    ax = plt.gca()
    for i, condition in enumerate(conditions):
        df_condition = summary_df[summary_df['Condition'] == condition]
        color = palette[i]
        
        ax.fill_between(x=df_condition['Generation'],
                        y1=df_condition['group_mean'] - (df_condition['group_sd'] ** 1/5),
                        y2=df_condition['group_mean'] + (df_condition['group_sd'] ** 1/5),
                        color=color, alpha=0.3)
    plt.title(f'Weighted Average Bits of {csv_type[3]} Over Time')
    plt.ylabel(f'Weighted Average Bits of {csv_type[3]}')
    plt.grid(False)
    plt.savefig(join_path(args.output_folder, f'Weighted_Average_{csv_type[3]}.png'))

    tot_mem_bits_df = bits_of_memory_df.groupby(['Generation'], observed=True).agg(
        group_mean=('Mean', 'mean'),
        group_sd=('Mean', 'std')
    ).reset_index()

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=tot_mem_bits_df, x='Generation', y='group_mean', hue='group_mean', markers=False, dashes=True, palette=plt.colormaps["viridis"])
    sns.lineplot(data=dll_df, x='Generation', y='group_mean', hue='Condition', style='Condition', markers=False, dashes=False, err_style="band", errorbar='ci', palette=palette)
    ax = plt.gca()
    for i, condition in enumerate(conditions):
        df_condition = dll_df[dll_df['Condition'] == condition]
        color = palette[i]
        
        ax.fill_between(x=df_condition['Generation'],
                        y1=df_condition['group_mean'] - (df_condition['group_sd'] ** 1/5),
                        y2=df_condition['group_mean'] + (df_condition['group_sd'] ** 1/5),
                        color=color, alpha=0.3)
    plt.title(f'Average Decision List Length Over Time')
    plt.ylabel(f'Average Decision List Length')
    plt.grid(False)
    plt.savefig(join_path(args.output_folder, f'Average_Decision_List_Length_with_Mem_{csv_type[3]}.png'))

    tot_mem_bits_df.loc[tot_mem_bits_df['group_mean'] == np.min(tot_mem_bits_df['group_mean']), 'group_mean'] = tot_mem_bits_df['group_mean'].mean()
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=tot_mem_bits_df, x='Generation', y='group_mean', markers=False, dashes=False)
    plt.title(f'Total Memory Bits Over Time')
    plt.ylabel(f'Total Memory Bits')
    plt.grid(False)
    plt.savefig(join_path(args.output_folder, f'Mem_Bits_Overtime_{csv_type[3]}.png'))

    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=summary_df, x='Generation', y='group_mean', hue='Condition', style='Condition', markers=False, dashes=False, palette=palette)
    plt.title(f'Weighted Average Bits of {csv_type[3]} Over Time')
    plt.ylabel(f'Weighted Average Bits of {csv_type[3]}')
    plt.grid(False)
    plt.savefig(join_path(args.output_folder, f'Weighted Average_{csv_type[3]}_NoDashes.png'))

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=summary_df, x='Generation', y='group_mean', hue='Condition', style='Condition', markers=False, dashes=False, palette=palette)
    sns.lineplot(data=tot_mem_bits_df, x='Generation', y='group_mean', hue='group_mean', markers=False, dashes=True, palette=plt.colormaps["viridis"])
    plt.title(f'Average Decision List Length Over Time')
    plt.ylabel(f'Average Decision List Length')
    plt.grid(False)
    plt.savefig(join_path(args.output_folder, f'Average_Decision_List_Length_with_Mem_No_Dashes_{csv_type[3]}.png'))

    plt.figure(figsize=(10, 6))
    plt.hist(bits_of_memory_df['Mean'], bins=30)
    plt.title(f'Distribution of Mean Bits of {csv_type[3]}')
    plt.xlabel(f'Mean Bits of {csv_type[3]}')
    plt.ylabel('Frequency')
    plt.savefig(join_path(args.output_folder, f'Mean_{csv_type[3]}.png'))

    forward_df = pd.concat([summary_df['group_mean'], dll_df['group_mean']], axis=1)
    inv_df = pd.concat([dll_df['group_mean'], summary_df['group_mean']], axis=1)
    with open(join_path(args.output_folder, "stat_output.txt"), "a") as f:
        f.write("########################################################################################################")
        f.write("#####################################        Correlation       #########################################")
        f.write("##############################       Memory versus Decision List Length         ########################")
        f.write("########################################################################################################")
        try:
            pearson_corr = summary_df['group_mean'].corr(dll_df['group_mean'], method='pearson')
            f.writelines(f'{csv_type[3].upper()} - Pearson Correlation test results: {pearson_corr}')
            f.write('\n')
        except:
            f.write(f"{csv_type[3].upper()} - Pearson Correlation test failed, column mismatch likely")
            f.write('\n')
            print(f"{csv_type[3].upper()} - Pearson Correlation test failed, column mismatch likely", flush=True)
        try:
            pearson_inv = dll_df['group_mean'].corr(summary_df['group_mean'], method='pearson')
            f.writelines(f'{csv_type[3].upper()} - Pearson Inverse test results: {pearson_inv}')
            f.write('\n')
        except:
            f.write(f"{csv_type[3].upper()} - Pearson Inverse test failed, column mismatch likely")
            f.write('\n')
            print(f"{csv_type[3].upper()} - Pearson Inverse test failed, column mismatch likely", flush=True)

        try:
            spearman_corr = summary_df['group_mean'].corr(dll_df['group_mean'], method='spearman')
            f.writelines(f'{csv_type[3].upper()} - Spearman Correlation test results: {spearman_corr}')
            f.write('\n')
        except:
            f.write(f"{csv_type[3].upper()} - Spearman Correlation test failed, column mismatch likely")
            f.write('\n')
            print(f"{csv_type[3].upper()} - Spearman Correlation test failed, column mismatch likely", flush=True)
        
        try:
            spearman_inv = dll_df['group_mean'].corr(summary_df['group_mean'], method='spearman')
            f.writelines(f'{csv_type[3].upper()} - Spearman Inverse test results: {spearman_inv}')
            f.write('\n')
        except:
            f.write(f"{csv_type[3].upper()} - Spearman Inverse test failed, column mismatch likely")
            f.write('\n')
            print(f"{csv_type[3].upper()} - Spearman Inverse test failed, column mismatch likely", flush=True)
        try:
            granger_caus = grangercausalitytests(forward_df, maxlag=2, verbose=True)
            f.writelines(f'{csv_type[3].upper()} - Granger Causality test results: {granger_caus}')
            f.write('\n')
        except:
            f.write(f"{csv_type[3].upper()} - Granger Causality test failed, column mismatch likely")
            f.write('\n')
            print(f"{csv_type[3].upper()} - Granger Causality test failed, column mismatch likely", flush=True)
        try:
            granger_inv = grangercausalitytests(inv_df, maxlag=2, verbose=True)
            f.writelines(f'{csv_type[3].upper()} - Granger Inverse test results: {granger_inv}')
            f.write('\n')
        except:
            f.write(f"{csv_type[3].upper()} - Granger Inverse test failed, column mismatch likely")
            f.write('\n')
            print(f"{csv_type[3].upper()} - Granger Inverse test failed, column mismatch likely", flush=True)
        f.write("########################################################################################################")
        f.write("#####################################     Multi-Comparison     #########################################")
        f.write("########################################################################################################")
        try:
            anova_results = stats.f_oneway(*[group['Mean'].values for name, group in bits_of_memory_df.groupby('Condition', observed=True)])
            f.writelines(f'{csv_type[3].upper()} - ANOVA test results: {anova_results}')
            f.write('\n')
        except:
            f.write(f"{csv_type[3].upper()} - ANOVA test failed, column mismatch likely")
            f.write('\n')
            print(f"{csv_type[3].upper()} - ANOVA test failed, column mismatch likely", flush=True)

        try:
            tukey_results = pairwise_tukeyhsd(bits_of_memory_df['Mean'], bits_of_memory_df['Condition'])
            f.writelines(f'{csv_type[3].upper()} - Tukey test results: {tukey_results}')
            f.write('\n')
        except:
            f.write(f"{csv_type[3].upper()} - Tukey test failed, likely, column mismatch likely")
            f.write('\n')
            print(f"{csv_type[3].upper()} - Tukey test failed, likely, column mismatch likely", flush=True)

        try:
            kruskal_data = bits_of_memory_df[bits_of_memory_df['Generation'] == int(args.number_of_generations) - 1]
            kruskal_results = stats.kruskal(*[group['Mean'].values for name, group in kruskal_data.groupby('Condition', observed=True)])
            f.writelines(f"{csv_type[3].upper()} - Kruskal-Wallis test results: {kruskal_results}")
            f.write('\n')
        except:
            f.write(f"{csv_type[3].upper()} - Kruskal-Wallis Test Failed, results likely identical or column mismatch likely")
            f.write('\n')
            print(f"{csv_type[3].upper()} - Kruskal-Wallis Test Failed, results likely identical or column mismatch likely", flush=True)

        try:
            comparison = MultiComparison(kruskal_data['Mean'], kruskal_data['Condition'])
            wilcox_results = comparison.allpairtest(stats.mannwhitneyu, method='bonferroni')
            f.writelines(f"{csv_type[3].upper()} - Bonferroni-Corrected Kruskal/Wilcox Test Results: {wilcox_results[0]}")
            f.write('\n')
        except:
            f.write(f"{csv_type[3].upper()} - Wilcox Test Failed, results likely identical or column mismatch likely")
            f.write('\n')
            print(f"{csv_type[3].upper()} - Wilcox Test Failed, results likely identical or column mismatch likely", flush=True)
    f.close()

def strat_freq(args):
    print("Constructing Strategy Frequency Plot")
    strategies_df = pd.read_csv(join_path(str(args.output_folder), "strategies_df.csv"), header=None)
    column_names = ['Row_Label'] + list(range(len(strategies_df.columns[1:-2]))) + ['Condition', 'Strategy']
    strategies_df.columns = column_names

    strategies_df.drop('Row_Label', axis=1, inplace=True)
    strategies_df = pd.melt(strategies_df, id_vars=['Condition', 'Strategy'], var_name='Generation', value_name='Frequency')
    strategies_df['Generation'] = pd.to_numeric(strategies_df['Generation'])
    strategies_df['Frequency'] = pd.to_numeric(strategies_df['Frequency'])

    plt.figure(figsize=(10, 6)) 
    sns.lineplot(data=strategies_df, x='Generation', y='Frequency', hue='Strategy', palette='tab10')
    plt.title("Strategy Frequency")
    plt.grid(False) 
    plt.gca().set_facecolor('white') 
    plt.legend().set_visible(True)  
    plt.tight_layout()  
    plt.savefig(join_path(str(args.output_folder), "Strategy_Frequency_Plot.png"))  

def common_strats(output_folder):
    print("Constructing Common Strategy Plot")
    most_common_strategy = pd.read_csv(join_path(output_folder, "most_common.csv"))
    #File currently saves Condition with a space in front
    most_common_strategy[' Condition'] = pd.to_numeric(most_common_strategy[' Condition'], errors='coerce') 
    most_common_strategy['Common_Strategy'] = most_common_strategy['Common_Strategy'].astype(str)

    subset_data = most_common_strategy[(most_common_strategy[' Condition'] != -0.5) & (most_common_strategy[' Condition'] != 0.0)]
    dat = subset_data.pivot_table(index='Common_Strategy', columns=' Condition', aggfunc='size', fill_value=0)
    dat_melt = dat.reset_index().melt(id_vars='Common_Strategy', var_name=' Condition', value_name='Frequency')

    order = dat_melt['Common_Strategy'].value_counts().nlargest(4).index.tolist()
    dat_melt = dat_melt[dat_melt['Common_Strategy'].isin(order)]
    dat_melt['Common_Strategy'] = pd.Categorical(dat_melt['Common_Strategy'], categories=order, ordered=True)
    dat_melt.sort_values(by='Common_Strategy', inplace=True)

    plt.figure(figsize=(12, 8))
    sns.barplot(x='Common_Strategy', y='Frequency', data=dat_melt) #, hue=' Condition' , dodge=True , palette=["#8CF582", "#82F5EB", "#828BF5", "#82B5EF"]
    plt.title('Most Common Strategies')
    plt.xticks(rotation=10)
    plt.xlabel('Strategy')
    plt.ylabel('Frequency')
    plt.grid(axis='y')

    for container in plt.gca().containers:
        plt.bar_label(container, label_type='edge')
    plt.savefig(join_path(output_folder, "Most_Common_Strategies.png"))

def main():
    arg_parser = argparse.ArgumentParser(
        description='Plotting function for handling DataFrames.')
    
    # Expects 1 argument: output folder
    arg_parser.add_argument("-o", "--output_folder", type=str, default="tests/pd_temp")
    arg_parser.add_argument("--output_frequency", type=int, default=10)
    arg_parser.add_argument("--number_of_generations", type=int, default=500)
    args = arg_parser.parse_args()
    if 'hybrid' in args.output_folder: csv_list = ['all_bits_df_Memory_comp_more_values.csv', 'all_bits_df_Summary_comp_more_values.csv', \
                'all_bits_df_Total_comp_more_values.csv']
    else: csv_list = ['all_bits_df_Memory_comp_more_values.csv']
    if os.path.exists(join_path(args.output_folder, "stat_output.txt")):
        os.remove(join_path(args.output_folder, "stat_output.txt"))
    for csv in csv_list:
        average_mem(args, csv)
    average_dll(args)
    strat_freq(args)
    common_strats(args.output_folder)
    

if __name__ == "__main__":
    main()

