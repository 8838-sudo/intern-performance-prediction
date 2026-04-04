import numpy as np
import pandas as pd
import os

def generate_intern_data(num_samples=1000, output_file='intern_data.csv'):
    np.random.seed(42)
    
    # Generate features
    # Assuming realistic ranges for intern metrics (0.0 to 1.0)
    # Generate features with full ranges (0.0 to 1.0)
    task_completion_rate = np.random.uniform(0.0, 1.0, num_samples)
    consistency_score = np.random.uniform(0.0, 1.0, num_samples)
    engagement_metric = np.random.uniform(0.0, 1.0, num_samples)
    
    # Increase proportion of low-performers by adding manual "low" records
    low_samples = int(num_samples * 0.15)
    task_completion_rate[:low_samples] = np.random.uniform(0.0, 0.3, low_samples)
    consistency_score[:low_samples] = np.random.uniform(0.0, 0.3, low_samples)
    engagement_metric[:low_samples] = np.random.uniform(0.0, 0.3, low_samples)
    
    # Generate target variable (Performance Score: 0-100)
    # Weighted base score
    base_score = (
        (task_completion_rate * 40) + 
        (consistency_score * 35) + 
        (engagement_metric * 25)
    )
    # Add random noise to simulate real-world variance
    noise = np.random.normal(0, 5, num_samples)
    performance_score = np.clip(base_score + noise, 0, 100)
    
    # Create DataFrame
    data = pd.DataFrame({
        'task_completion_rate': task_completion_rate,
        'consistency_score': consistency_score,
        'engagement_metric': engagement_metric,
        'performance_score': performance_score
    })
    
    # Save to CSV
    data.to_csv(output_file, index=False)
    print(f"Generated {num_samples} records and saved to {output_file}")

if __name__ == '__main__':
    generate_intern_data()
