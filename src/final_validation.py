import pandas as pd
import os

def validate():
    print("Final Validation Started...")
    
    # 1. Check Dataset
    dataset_path = 'Vector_Team_dataset.csv'
    if os.path.exists(dataset_path):
        df = pd.read_csv(dataset_path)
        print(f"✓ Dataset found: {len(df)} rows")
    else:
        print("✗ Dataset NOT found")
        
    # 2. Check Notebooks
    for nb in ['eda.ipynb', 'modeling.ipynb']:
        if os.path.exists(nb):
            print(f"✓ Notebook found: {nb}")
        else:
            print(f"✗ Notebook NOT found: {nb}")
            
    # 3. Check Report
    report_path = 'Vector_Team_Report.pdf'
    if os.path.exists(report_path):
        print(f"✓ Report found: {report_path}")
    else:
        print("✗ Report NOT found")

if __name__ == "__main__":
    validate()
