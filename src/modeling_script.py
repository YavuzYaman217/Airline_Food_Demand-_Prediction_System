import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import os

# Set style
sns.set_theme(style="whitegrid")

# Load data
df = pd.read_csv('Vector_Team_dataset.csv')

# Prepare features and target
X = df.drop(['flight_id', 'total_food_demand'], axis=1)
y = df['total_food_demand']

# Split data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Results storage
results = []

# 1. Baseline Model (Mean Predictor)
y_pred_baseline = np.full_like(y_test, y_train.mean())
results.append({
    'Model': 'Baseline (Mean)',
    'R2': r2_score(y_test, y_pred_baseline),
    'MAE': mean_absolute_error(y_test, y_pred_baseline),
    'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_baseline))
})

# 2. Linear Regression Model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)
results.append({
    'Model': 'Linear Regression',
    'R2': r2_score(y_test, y_pred_lr),
    'MAE': mean_absolute_error(y_test, y_pred_lr),
    'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_lr))
})

# 3. Alternative Model: Random Forest Regressor (with Hyperparameter Tuning - Bonus)
rf_params = {
    'n_estimators': [100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5]
}
rf_grid = GridSearchCV(RandomForestRegressor(random_state=42), rf_params, cv=3, scoring='neg_mean_squared_error')
rf_grid.fit(X_train, y_train)
best_rf = rf_grid.best_estimator_
y_pred_rf = best_rf.predict(X_test)

results.append({
    'Model': 'Random Forest (Tuned)',
    'R2': r2_score(y_test, y_pred_rf),
    'MAE': mean_absolute_error(y_test, y_pred_rf),
    'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_rf))
})

# Save results table
results_df = pd.DataFrame(results)
results_df.to_csv('plots/model_comparison.csv', index=False)

# Visualizations for Modeling
os.makedirs('plots', exist_ok=True)

# Actual vs Predicted (Linear Regression)
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_lr, alpha=0.5, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Food Demand')
plt.ylabel('Predicted Food Demand')
plt.title('Linear Regression: Actual vs Predicted')
plt.savefig('plots/lr_actual_vs_predicted.png')
plt.close()

# Actual vs Predicted (Random Forest)
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_rf, alpha=0.5, color='green')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Food Demand')
plt.ylabel('Predicted Food Demand')
plt.title('Random Forest: Actual vs Predicted')
plt.savefig('plots/rf_actual_vs_predicted.png')
plt.close()

# Feature Importance (Random Forest)
plt.figure(figsize=(10, 6))
importances = best_rf.feature_importances_
feat_importances = pd.Series(importances, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.title('Random Forest: Feature Importance')
plt.savefig('plots/feature_importance.png')
plt.close()

# Residual Plot (Best Model - RF)
plt.figure(figsize=(10, 6))
residuals = y_test - y_pred_rf
sns.histplot(residuals, kde=True, color='purple')
plt.title('Residual Distribution (Random Forest)')
plt.xlabel('Prediction Error')
plt.savefig('plots/residuals_distribution.png')
plt.close()

# Bonus: Business Cost Analysis
# Cost = (OverPredictions * $5) + (UnderPredictions * $20)
def calculate_cost(actual, predicted):
    errors = predicted - actual
    over = np.sum(errors[errors > 0] * 5)
    under = np.sum(np.abs(errors[errors < 0]) * 20)
    return over + under

cost_baseline = calculate_cost(y_test, y_pred_baseline)
cost_lr = calculate_cost(y_test, y_pred_lr)
cost_rf = calculate_cost(y_test, y_pred_rf)

costs = pd.DataFrame({
    'Model': ['Baseline', 'Linear Regression', 'Random Forest'],
    'Total Cost ($)': [cost_baseline, cost_lr, cost_rf]
})
costs.to_csv('plots/business_cost_analysis.csv', index=False)

print("Modeling completed. Results and plots saved.")
