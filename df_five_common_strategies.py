import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

most_common_strategy = pd.read_csv("most_common.csv")
print(most_common_strategy)
#File currentl saves Condition with a space in front
most_common_strategy[' Condition'] = pd.to_numeric(most_common_strategy[' Condition'], errors='coerce') 
most_common_strategy['Common_Strategy'] = most_common_strategy['Common_Strategy'].astype(str)

subset_data = most_common_strategy[(most_common_strategy[' Condition'] != -0.5) & (most_common_strategy[' Condition'] != 0.0)]
dat = subset_data.pivot_table(index='Common_Strategy', columns=' Condition', aggfunc='size', fill_value=0)
dat_melt = dat.reset_index().melt(id_vars='Common_Strategy', var_name=' Condition', value_name='Frequency')

order = ["0~~", "00~1~", "01~1~", "0001~11~"]
dat_melt['Common_Strategy'] = pd.Categorical(dat_melt['Common_Strategy'], categories=order, ordered=True)

plt.figure(figsize=(10, 6))
sns.barplot(x='Common_Strategy', y='Frequency', data=dat_melt, palette=["#8CF582", "#82F5EB", "#828BF5", "#82B5EF"]) #,hue=' Condition', dodge=True, palette=["#8CF582", "#82F5EB", "#828BF5"]
plt.title('Most Common Strategies')
plt.xlabel('Strategy')
plt.ylabel('Frequency')
plt.legend(title='Condition')
plt.grid(axis='y')

for container in plt.gca().containers:
    plt.bar_label(container, label_type='edge')
plt.savefig("Most_Common_Strategies_Static_Competitor_More_Values.pdf")
