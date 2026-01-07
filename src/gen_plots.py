# import pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_theme(style="whitegrid")
os.makedirs('plots', exist_ok=True)

# Data from polished execution
costs = pd.DataFrame({
    'Model': ['Baseline', 'Linear Regression', 'Random Forest', 'Gradient Boosting'],
    'Total Cost ($)': [1604105, 501532, 112756, 108917]
})

# Business Cost Bar Chart
plt.figure(figsize=(10, 6))
sns.barplot(x='Model', y='Total Cost ($)', data=costs, palette='viridis')
plt.title('Business Cost Analysis: Financial Impact of Forecast Errors')
plt.ylabel('Total Cost ($)')
plt.savefig('plots/business_cost_analysis.png')
plt.close()

print("Plots generated successfully.")
