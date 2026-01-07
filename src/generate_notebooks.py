import nbformat as nbf
import os

def create_eda_notebook():
    nb = nbf.v4.new_notebook()
    
    cells = [
        nbf.v4.new_markdown_cell("# Havayolu Yemek Talebi Tahmini - Keşifsel Veri Analizi (EDA)\n**Takım Adı:** Vector_Team"),
        nbf.v4.new_markdown_cell("Bu not defteri, Havayolu Yemek Talebi Tahmini projesi için sentetik veri setinin oluşturulmasını ve keşifsel veri analizini (EDA) içermektedir."),
        nbf.v4.new_code_cell(
            "import pandas as pd\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n"
            "import os\n\n"
            "# Set style\n"
            "sns.set_theme(style='whitegrid')\n\n"
            "# Create output directory for plots\n"
            "os.makedirs('plots', exist_ok=True)"
        ),
        nbf.v4.new_markdown_cell("## 1. Sentetik Veri Seti Oluşturma\nProje gereksinimlerine uygun olarak sentetik bir veri seti oluşturulacaktır."),
        nbf.v4.new_code_cell(
            "def generate_airline_data(n_rows=5000):\n"
            "    np.random.seed(42)\n"
            "    flight_ids = np.arange(1, n_rows + 1)\n"
            "    passenger_counts = np.random.randint(50, 301, size=n_rows)\n"
            "    adult_passengers = []\n"
            "    child_passengers = []\n"
            "    for count in passenger_counts:\n"
            "        adult = np.random.randint(int(count * 0.7), count + 1)\n"
            "        adult_passengers.append(adult)\n"
            "        child_passengers.append(count - adult)\n"
            "    adult_passengers = np.array(adult_passengers)\n"
            "    child_passengers = np.array(child_passengers)\n"
            "    is_international = np.random.choice([0, 1], size=n_rows, p=[0.8, 0.2])\n"
            "    flight_durations = []\n"
            "    for inter in is_international:\n"
            "        duration = np.random.uniform(3, 12) if inter == 1 else np.random.uniform(1, 8)\n"
            "        flight_durations.append(round(duration, 2))\n"
            "    flight_durations = np.array(flight_durations)\n"
            "    business_class_ratios = np.random.uniform(0, 1.0, size=n_rows)\n\n"
            "    total_food_demand = []\n"
            "    base_meals_per_passenger = 1.0\n"
            "    for i in range(n_rows):\n"
            "        dur = flight_durations[i]\n"
            "        inter = is_international[i]\n"
            "        biz_ratio = business_class_ratios[i]\n"
            "        p_count = passenger_counts[i]\n"
            "        c_count = child_passengers[i]\n"
            "        if dur < 2: duration_multiplier = 0.8\n"
            "        elif dur < 4: duration_multiplier = 1.0\n"
            "        elif dur < 8: duration_multiplier = 1.5\n"
            "        else: duration_multiplier = 2.0\n"
            "        international_bonus = 0.3 if inter == 1 else 0.0\n"
            "        business_bonus = biz_ratio * 0.4\n"
            "        child_ratio = c_count / p_count\n"
            "        child_reduction = child_ratio * 0.15\n"
            "        food_per_passenger = base_meals_per_passenger * duration_multiplier * (1 + international_bonus + business_bonus - child_reduction)\n"
            "        demand = round(p_count * food_per_passenger)\n"
            "        demand = max(demand, int(p_count * 0.5))\n"
            "        total_food_demand.append(demand)\n\n"
            "    df = pd.DataFrame({\n"
            "        'flight_id': flight_ids,\n"
            "        'flight_duration': flight_durations,\n"
            "        'passenger_count': passenger_counts,\n"
            "        'adult_passengers': adult_passengers,\n"
            "        'child_passengers': child_passengers,\n"
            "        'business_class_ratio': business_class_ratios,\n"
            "        'is_international': is_international,\n"
            "        'total_food_demand': total_food_demand\n"
            "    })\n"
            "    return df\n\n"
            "df = generate_airline_data(5000)\n"
            "df.to_csv('Vector_Team_dataset.csv', index=False)\n"
            "print('Dataset generated successfully: Vector_Team_dataset.csv')"
        ),
        nbf.v4.new_markdown_cell("## 2. Keşifsel Veri Analizi (EDA)"),
        nbf.v4.new_code_cell(
            "df = pd.read_csv('Vector_Team_dataset.csv')\n"
            "print(df.describe())\n"
            "print(df.isnull().sum())\n\n"
            "plt.figure(figsize=(10, 8))\n"
            "sns.heatmap(df.drop('flight_id', axis=1).corr(), annot=True, cmap='coolwarm', center=0)\n"
            "plt.title('Feature Correlation Heatmap')\n"
            "plt.show()\n\n"
            "fig, axes = plt.subplots(1, 2, figsize=(16, 6))\n"
            "sns.scatterplot(data=df, x='passenger_count', y='total_food_demand', hue='is_international', alpha=0.5, ax=axes[0])\n"
            "axes[0].set_title('Passenger Count vs Total Food Demand')\n"
            "sns.scatterplot(data=df, x='flight_duration', y='total_food_demand', hue='is_international', alpha=0.5, ax=axes[1])\n"
            "axes[1].set_title('Flight Duration vs Total Food Demand')\n"
            "plt.show()"
        )
    ]
    
    nb.cells = cells
    with open('eda.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

def create_modeling_notebook():
    nb = nbf.v4.new_notebook()
    
    cells = [
        nbf.v4.new_markdown_cell("# Havayolu Yemek Talebi Tahmini - Modelleme ve Karşılaştırma\n**Takım Adı:** Vector_Team"),
        nbf.v4.new_code_cell(
            "import pandas as pd\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n"
            "from sklearn.model_selection import train_test_split, GridSearchCV\n"
            "from sklearn.linear_model import LinearRegression\n"
            "from sklearn.ensemble import RandomForestRegressor\n"
            "from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error\n\n"
            "df = pd.read_csv('Vector_Team_dataset.csv')\n"
            "X = df.drop(['flight_id', 'total_food_demand'], axis=1)\n"
            "y = df['total_food_demand']\n"
            "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\n"
            "results = []\n"
            "y_pred_baseline = np.full_like(y_test, y_train.mean())\n"
            "results.append({'Model': 'Baseline', 'R2': r2_score(y_test, y_pred_baseline), 'MAE': mean_absolute_error(y_test, y_pred_baseline), 'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_baseline))})\n\n"
            "lr = LinearRegression()\n"
            "lr.fit(X_train, y_train)\n"
            "y_pred_lr = lr.predict(X_test)\n"
            "results.append({'Model': 'Linear Regression', 'R2': r2_score(y_test, y_pred_lr), 'MAE': mean_absolute_error(y_test, y_pred_lr), 'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_lr))})\n\n"
            "rf = RandomForestRegressor(n_estimators=100, random_state=42)\n"
            "rf.fit(X_train, y_train)\n"
            "y_pred_rf = rf.predict(X_test)\n"
            "results.append({'Model': 'Random Forest', 'R2': r2_score(y_test, y_pred_rf), 'MAE': mean_absolute_error(y_test, y_pred_rf), 'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_rf))})\n\n"
            "print(pd.DataFrame(results))"
        )
    ]
    
    nb.cells = cells
    with open('modeling.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)

if __name__ == "__main__":
    create_eda_notebook()
    create_modeling_notebook()
    print("Notebooks generated successfully.")
