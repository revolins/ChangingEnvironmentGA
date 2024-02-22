import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Loading the data
bits_of_memory_df = pd.read_csv("all_bits_df_static_comp_more_values.csv")

# Updating column names and data types
# Dropping the 'Row_Label' column
#bits_of_memory_df.drop(columns='Row_Label', inplace=True)

# Converting 'Generation' and 'Condition' to numeric, 'Condition' also to categorical
print(bits_of_memory_df.columns.tolist())
bits_of_memory_df['Generation'] = pd.to_numeric(bits_of_memory_df['Generation'], errors='coerce')
bits_of_memory_df['Condition'] = pd.Categorical(pd.to_numeric(bits_of_memory_df['Condition'], errors='coerce'))

# Converting B0, B1, B2, B3, B4 to numeric
for col in ['Organisms With 0 Bits of Memory', 'Organisms With 1 Bits of Memory', 'Organisms With 2 Bits of Memory', 'Organisms With 3 Bits of Memory', 'Organisms With 4 Bits of Memory']:
    bits_of_memory_df[col] = pd.to_numeric(bits_of_memory_df[col], errors='coerce')

# Calculating the weighted mean
weights = np.arange(5)
bits_of_memory_df['Mean'] = bits_of_memory_df.apply(lambda row: np.average(row[:5], weights=weights), axis=1)

# Aggregating to find mean and standard deviation for each Condition and Generation
summary_df = bits_of_memory_df.groupby(['Condition', 'Generation']).agg(group_mean=('Mean', 'mean'), group_sd=('Mean', 'std')).reset_index()

# Plotting
plt.figure(figsize=(10, 6))
sns.lineplot(data=summary_df, x='Generation', y='group_mean', hue='Condition', style='Condition', markers=True, dashes=False, err_style="band", ci='sd')
plt.title('Average Bits of Memory Over Time')
plt.xlabel('Generation')
plt.ylabel('Average Bits of Memory')
plt.legend(title='Condition')
plt.tight_layout()
plt.savefig("Average_Bits_Memory_Overtime_Static_Comp.pdf")

# Filtering for specific conditions and plotting
filtered_conditions = [0, 0.01, 0.03, 0.05, 0.075]
filtered_df = summary_df[summary_df['Condition'].isin(filtered_conditions)]

plt.figure(figsize=(10, 6))
sns.lineplot(data=filtered_df, x='Generation', y='group_mean', hue='Condition', palette=['#F5828C', '#8CF582', '#82F5EB', '#828BF5'], style='Condition', markers=True, dashes=False, err_style="band", ci='sd')
plt.title('Average Bits of Memory Over Time (Restricted Conditions)')
plt.xlabel('Generation')
plt.ylabel('Average Bits of Memory')
plt.legend(title='Condition')
plt.tight_layout()
plt.savefig("Average_Bits_Memory_Overtime_Restricted_Static_Comp.pdf")

# Histogram to check assumptions
plt.figure(figsize=(8, 6))
plt.hist(bits_of_memory_df['Mean'], bins=20)
plt.title('Histogram of Mean Bits of Memory')
plt.xlabel('Mean Bits of Memory')
plt.ylabel('Frequency')
plt.show()

# Statistical tests
# Kruskal-Wallis Test
end_df = bits_of_memory_df[bits_of_memory_df['Generation'] == 499]
kruskal_result = stats.kruskal(*[group["Mean"].values for name, group in end_df.groupby("Condition")])
print(kruskal_result)

# Pairwise Wilcoxon (Mann-Whitney) tests with Bonferroni correction
condition_combinations = end_df['Condition'].unique().tolist()
pairwise_results = {}
for i in range(len(condition_combinations)):
    for j in range(i+1, len(condition_combinations)):
        group1 = end_df[end_df['Condition'] == condition_combinations[i]]['Mean']
        group2 = end_df[end_df['Condition'] == condition_combinations[j]]['Mean']
        stat, p = stats.mannwhitneyu(group1, group2, alternative='two-sided')
        # Adjust p-value for multiple testing using Bonferroni correction
        p_adjusted = p * (len(condition_combinations) * (len(condition_combinations) - 1) / 2)
        pairwise_results[f"{condition_combinations[i]} vs {condition_combinations[j]}"] = p_adjusted

print(pairwise_results)
