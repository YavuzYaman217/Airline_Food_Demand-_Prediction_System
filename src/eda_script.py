import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_theme(style="whitegrid")

# Load data
df = pd.read_csv('Vector_Team_dataset.csv')

# Create output directory for plots
os.makedirs('plots', exist_ok=True)

# 1. Basic Statistics
stats = df.describe()
stats.to_csv('plots/basic_statistics.csv')

# 2. Missing Values
missing = df.isnull().sum()
missing.to_csv('plots/missing_values.csv')

# 3. Correlation Heatmap
plt.figure(figsize=(10, 8))
correlation = df.drop('flight_id', axis=1).corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Feature Correlation Heatmap')
plt.savefig('plots/correlation_heatmap.png')
plt.close()

# 4. Distributions (Histograms)
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
sns.histplot(df['passenger_count'], kde=True, ax=axes[0, 0], color='skyblue')
axes[0, 0].set_title('Distribution of Passenger Count')

sns.histplot(df['flight_duration'], kde=True, ax=axes[0, 1], color='salmon')
axes[0, 1].set_title('Distribution of Flight Duration')

sns.histplot(df['total_food_demand'], kde=True, ax=axes[1, 0], color='green')
axes[1, 0].set_title('Distribution of Total Food Demand')

sns.countplot(x='is_international', data=df, ax=axes[1, 1], palette='viridis')
axes[1, 1].set_title('International vs Domestic Flights')
plt.tight_layout()
plt.savefig('plots/distributions.png')
plt.close()

# 5. Boxplots for Outliers
plt.figure(figsize=(12, 6))
sns.boxplot(data=df[['passenger_count', 'total_food_demand']])
plt.title('Boxplots for Passenger Count and Food Demand')
plt.savefig('plots/boxplots.png')
plt.close()

# 6. Scatter Plots (Relationships with Target)
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.scatterplot(data=df, x='passenger_count', y='total_food_demand', hue='is_international', alpha=0.5, ax=axes[0])
axes[0].set_title('Passenger Count vs Total Food Demand')

sns.scatterplot(data=df, x='flight_duration', y='total_food_demand', hue='is_international', alpha=0.5, ax=axes[1])
axes[1].set_title('Flight Duration vs Total Food Demand')
plt.tight_layout()
plt.savefig('plots/scatter_plots.png')
plt.close()

print("EDA completed and plots saved in 'plots' directory.")
