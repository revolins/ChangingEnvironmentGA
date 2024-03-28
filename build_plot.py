import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) #For those pesky deprecation warnings

def average_mem():
    print("Constructing Memory Plots and Running Statistical Tests")
    bits_of_memory_df = pd.read_csv("pd_check/all_bits_df_static_comp_more_values.csv")
    bits_of_memory_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    print(bits_of_memory_df.columns.tolist())
    bits_of_memory_df.columns = ['Row_Label', 'B0', 'B1', 'B2', 'B3', 'B4', 'Condition', 'Generation']
    print(bits_of_memory_df.columns.tolist())
    bits_of_memory_df.drop(['Row_Label'], axis=1, inplace=True)
    bits_of_memory_df['Generation'] = pd.to_numeric(bits_of_memory_df['Generation'], errors='coerce')
    bits_of_memory_df['Condition'] = pd.Categorical(pd.to_numeric(bits_of_memory_df['Condition'], errors='coerce'))
    for col in ['B0', 'B1', 'B2', 'B3', 'B4']:
        bits_of_memory_df[col] = pd.to_numeric(bits_of_memory_df[col], errors='coerce')

    weights = np.arange(5)
    bits_of_memory_df['Mean'] = bits_of_memory_df.apply(lambda row: np.average(row[:5], weights=weights), axis=1)

    summary_df = bits_of_memory_df.groupby(['Condition', 'Generation'], observed=True).agg(
        group_mean=('Mean', 'mean'),
        group_sd=('Mean', 'std')
    ).reset_index()

    conditions = summary_df['Condition'].unique()

    palette = sns.color_palette("husl", len(conditions))
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=summary_df, x='Generation', y='group_mean', hue='Condition', style='Condition', markers=False, dashes=False, err_style="band", errorbar='ci', palette=palette)
    ax = plt.gca()
    for i, condition in enumerate(conditions):
        df_condition = summary_df[summary_df['Condition'] == condition]
        color = palette[i]
        
        ax.fill_between(x=df_condition['Generation'],
                        y1=df_condition['group_mean'] - df_condition['group_sd'],
                        y2=df_condition['group_mean'] + df_condition['group_sd'],
                        color=color, alpha=0.3)
    plt.title('Average Bits of Memory Over Time')
    plt.ylabel('Average Bits of Memory')
    plt.grid(False)
    plt.savefig('pd_check/Average_Memory.png')

    palette = sns.color_palette("husl", len(conditions))
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=summary_df, x='Generation', y='group_mean', hue='Condition', style='Condition', markers=False, dashes=False, palette=palette)
    plt.title('Average Bits of Memory Over Time')
    plt.ylabel('Average Bits of Memory')
    plt.grid(False)
    plt.savefig('pd_check/Average_Memory_NoDashes.png')

    plt.figure(figsize=(10, 6))
    plt.hist(bits_of_memory_df['Mean'], bins=30)
    plt.title('Distribution of Mean Bits of Memory')
    plt.xlabel('Mean Bits of Memory')
    plt.ylabel('Frequency')
    plt.savefig('pd_check/Mean_Memory.png')

    try:
        anova_results = stats.f_oneway(*[group['Mean'].values for name, group in bits_of_memory_df.groupby('Condition', observed=True)])
        print(f'ANOVA test results: {anova_results}')
    except:
        print("ANOVA test failed, likely needs more tests")

    try:
        tukey_results = pairwise_tukeyhsd(bits_of_memory_df['Mean'], bits_of_memory_df['Condition'])
        print(tukey_results)
    except:
        print("Tukey test failed, likely needs more tests")

    try:
        kruskal_data = bits_of_memory_df[bits_of_memory_df['Generation'] == 499]
        kruskal_results = stats.kruskal(*[group['Mean'].values for name, group in kruskal_data.groupby('Condition', observed=True)])
        print(f'Kruskal-Wallis test results: {kruskal_results}')
    except:
        print("Kruskal-Wallis Test Failed, results likely identical - can be fixed with more tests")

    try:
        comparison = MultiComparison(kruskal_data['Mean'], kruskal_data['Condition'])
        wilcox_results = comparison.allpairtest(stats.mannwhitneyu, method='bonferroni')
        print(wilcox_results[0])
    except:
        print("Wilcox Test Failed, results likely identical - can be fixed with more tests")

def strat_freq():
    print("Constructing Strategy Frequency Plot")
    strategies_df = pd.read_csv("pd_check/strategies_df.csv", header=None)
    column_names = ['Row_Label'] + list(range(0, 501, 10)) + ['Condition', 'Strategy']
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
    plt.savefig("pd_check/Strategy_Frequency_Plot.png")  

def common_strats():
    print("Constructing Common Strategy Plot")
    most_common_strategy = pd.read_csv("pd_check/most_common.csv")
    print(most_common_strategy)
    #File currently saves Condition with a space in front
    most_common_strategy[' Condition'] = pd.to_numeric(most_common_strategy[' Condition'], errors='coerce') 
    most_common_strategy['Common_Strategy'] = most_common_strategy['Common_Strategy'].astype(str)

    subset_data = most_common_strategy[(most_common_strategy[' Condition'] != -0.5) & (most_common_strategy[' Condition'] != 0.0)]
    dat = subset_data.pivot_table(index='Common_Strategy', columns=' Condition', aggfunc='size', fill_value=0)
    dat_melt = dat.reset_index().melt(id_vars='Common_Strategy', var_name=' Condition', value_name='Frequency')

    order = ["0~~", "00~1~", "01~1~", "0001~11~"]
    dat_melt['Common_Strategy'] = pd.Categorical(dat_melt['Common_Strategy']) #, categories=order, ordered=True

    plt.figure(figsize=(12, 8))
    sns.barplot(x='Common_Strategy', y='Frequency', data=dat_melt) #, hue=' Condition' , dodge=True , palette=["#8CF582", "#82F5EB", "#828BF5", "#82B5EF"]
    plt.title('Most Common Strategies')
    plt.xticks(rotation=10)
    plt.xlabel('Strategy')
    plt.ylabel('Frequency')
    plt.legend().set_visible(True)
    plt.grid(axis='y')

    for container in plt.gca().containers:
        plt.bar_label(container, label_type='edge')
    plt.savefig("pd_check/Most_Common_Strategies.png")

average_mem()
strat_freq()
common_strats()