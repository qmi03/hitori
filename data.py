import pandas as pd
import numpy as np
df = pd.read_csv('hitori_metrics.csv')

print(df)
#df.drop_duplicates(subset=['Size','Difficulty','FunctionCalls'])

df['Time_group'] = df['Time'].apply(lambda x: round(x, 2))  # Round to nearest hundredth for example
grouped = df.groupby(['FunctionCalls', 'Time_group'])
print(grouped)
filtered_df = grouped.filter(lambda x: len(x) > 1)
print(filtered_df)