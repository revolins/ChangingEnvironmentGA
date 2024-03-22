import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd, MultiComparison

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning) #For those pesky deprecation warnings

bits_of_memory_df = pd.read_csv("all_bits_df_static_comp_more_values.csv")
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
plt.savefig('Average_Bits_Memory_Overtime_Static_Comp.pdf')

plt.figure(figsize=(10, 6))
plt.hist(bits_of_memory_df['Mean'], bins=30)
plt.title('Distribution of Mean Bits of Memory')
plt.xlabel('Mean Bits of Memory')
plt.ylabel('Frequency')
plt.savefig('Mean_Bits_Memory_Distribution_Check.png')

anova_results = stats.f_oneway(*[group['Mean'].values for name, group in bits_of_memory_df.groupby('Condition', observed=True)])
print(f'ANOVA test results: {anova_results}')

tukey_results = pairwise_tukeyhsd(bits_of_memory_df['Mean'], bits_of_memory_df['Condition'])
print(tukey_results)

kruskal_data = bits_of_memory_df[bits_of_memory_df['Generation'] == 499]
kruskal_results = stats.kruskal(*[group['Mean'].values for name, group in kruskal_data.groupby('Condition', observed=True)])
print(f'Kruskal-Wallis test results: {kruskal_results}')

comparison = MultiComparison(kruskal_data['Mean'], kruskal_data['Condition'])
wilcox_results = comparison.allpairtest(stats.mannwhitneyu, method='bonferroni')
print(wilcox_results[0])
