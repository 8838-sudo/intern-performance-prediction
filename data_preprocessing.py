import pandas as pd
import numpy as np
import os

def load_and_preprocess_data(input_file='intern_data.csv', output_file='clean_intern_data.csv'):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please run data_generator.py first.")
        return None
        
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    
    # 1. Handle missing values
    initial_shape = df.shape
    df.dropna(inplace=True)
    if df.shape != initial_shape:
        print(f"Dropped {initial_shape[0] - df.shape[0]} rows with missing values.")
        
    # 2. Check for outliers or invalid data bounds
    # Ensure features are between 0.0 and 1.0
    for col in ['task_completion_rate', 'consistency_score', 'engagement_metric']:
        df[col] = df[col].clip(0.0, 1.0)
        
    # Ensure performance score is between 0 and 100
    df['performance_score'] = df['performance_score'].clip(0.0, 100.0)
    
    print("\nData cleaning complete. Summary statistics:")
    print(df.describe())
    
    # Save clean data for training phase
    df.to_csv(output_file, index=False)
    print(f"\nCleaned dataset saved to {output_file}")
    return df

if __name__ == '__main__':
    load_and_preprocess_data()
