import pandas as pd
import numpy as np

def generate_airline_data(n_rows=5000):
    np.random.seed(42)
    
    # 1. flight_id
    flight_ids = np.arange(1, n_rows + 1)
    
    # 2. passenger_count (50-300)
    passenger_counts = np.random.randint(50, 301, size=n_rows)
    
    # 3. adult_passengers and child_passengers
    adult_passengers = []
    child_passengers = []
    for count in passenger_counts:
        adult = np.random.randint(int(count * 0.7), count + 1)
        adult_passengers.append(adult)
        child_passengers.append(count - adult)
    
    adult_passengers = np.array(adult_passengers)
    child_passengers = np.array(child_passengers)
    
    # 4. is_international (Binary 0/1)
    is_international = np.random.choice([0, 1], size=n_rows, p=[0.8, 0.2])
    
    # 5. flight_duration (1-12 hours)
    flight_durations = []
    for inter in is_international:
        if inter == 1:
            duration = np.random.uniform(3, 12)
        else:
            duration = np.random.uniform(1, 8)
        flight_durations.append(round(duration, 2))
    flight_durations = np.array(flight_durations)
    
    # 6. business_class_ratio (0-1)
    business_class_ratios = np.random.uniform(0, 1.0, size=n_rows)
    
    # 7. total_food_demand (Target Variable) - Using the specific formula from MD
    total_food_demand = []
    base_meals_per_passenger = 1.0
    
    for i in range(n_rows):
        dur = flight_durations[i]
        inter = is_international[i]
        biz_ratio = business_class_ratios[i]
        p_count = passenger_counts[i]
        c_count = child_passengers[i]
        
        # Factor 1: Flight duration effect
        if dur < 2:
            duration_multiplier = 0.8
        elif dur < 4:
            duration_multiplier = 1.0
        elif dur < 8:
            duration_multiplier = 1.5
        else:
            duration_multiplier = 2.0
            
        # Factor 2: International vs domestic
        international_bonus = 0.3 if inter == 1 else 0.0
        
        # Factor 3: Business class bonus
        business_bonus = biz_ratio * 0.4
        
        # Factor 4: Child reduction
        child_ratio = c_count / p_count
        child_reduction = child_ratio * 0.15
        
        # Final calculation
        food_per_passenger = base_meals_per_passenger * duration_multiplier * (1 + international_bonus + business_bonus - child_reduction)
        demand = round(p_count * food_per_passenger)
        
        # Ensure minimum constraint
        demand = max(demand, int(p_count * 0.5))
        total_food_demand.append(demand)
        
    df = pd.DataFrame({
        'flight_id': flight_ids,
        'flight_duration': flight_durations,
        'passenger_count': passenger_counts,
        'adult_passengers': adult_passengers,
        'child_passengers': child_passengers,
        'business_class_ratio': business_class_ratios,
        'is_international': is_international,
        'total_food_demand': total_food_demand
    })
    
    return df

def validate_dataset(df):
    """Validate that dataset meets all requirements"""
    checks = []
    check1 = (df['adult_passengers'] + df['child_passengers'] == df['passenger_count']).all()
    checks.append(("adult + child = total passengers", check1))
    check2 = ((df['business_class_ratio'] >= 0) & (df['business_class_ratio'] <= 1)).all()
    checks.append(("business_class_ratio in [0,1]", check2))
    check3 = ((df['flight_duration'] >= 1) & (df['flight_duration'] <= 12)).all()
    checks.append(("flight_duration in [1,12]", check3))
    check4 = (df[df['is_international'] == 1]['flight_duration'] >= 3).all()
    checks.append(("international flights >= 3h", check4))
    check5 = ((df['passenger_count'] >= 50) & (df['passenger_count'] <= 300)).all()
    checks.append(("passenger_count in [50,300]", check5))
    check6 = (df['total_food_demand'] >= df['passenger_count'] * 0.5).all()
    checks.append(("food_demand >= 0.5 * passengers", check6))
    check7 = len(df) >= 5000
    checks.append(("at least 5000 rows", check7))
    check8 = (df['is_international'].sum() / len(df)) >= 0.15
    checks.append(("at least 15% international", check8))
    short_flights = ((df['flight_duration'] >= 1) & (df['flight_duration'] <= 3)).sum()
    long_flights = ((df['flight_duration'] >= 8) & (df['flight_duration'] <= 12)).sum()
    check9 = (short_flights > 0) and (long_flights > 0)
    checks.append(("has short and long flights", check9))
    
    print("Dataset Validation Results:")
    print("=" * 50)
    for check_name, result in checks:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check_name}")
    print("=" * 50)
    return all(result for _, result in checks)

if __name__ == "__main__":
    df = generate_airline_data(5000)
    df.to_csv('Vector_Team_dataset.csv', index=False)
    print("Dataset generated successfully: Vector_Team_dataset.csv")
    validate_dataset(df)
