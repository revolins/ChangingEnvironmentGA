import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

strategies_df = pd.read_csv("strategies_df.csv", header=None)
column_names = ['Row_Label'] + list(range(0, 501, 10)) + ['Condition', 'Strategy']
strategies_df.columns = column_names

strategies_df.drop('Row_Label', axis=1, inplace=True)
strategies_df = pd.melt(strategies_df, id_vars=['Condition', 'Strategy'], var_name='Generation', value_name='Frequency')
strategies_df['Generation'] = pd.to_numeric(strategies_df['Generation'])
strategies_df['Frequency'] = pd.to_numeric(strategies_df['Frequency'])

plt.figure(figsize=(10, 6)) 
sns.lineplot(data=strategies_df, x='Generation', y='Frequency', hue='Strategy', palette='tab10')
plt.grid(False) 
plt.gca().set_facecolor('white') 
plt.legend().set_visible(True)  
plt.tight_layout()  
plt.savefig("Strategy_Frequency_Plot.pdf")  
