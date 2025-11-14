"""
Week 8: Data Poisoning Module
Introduces controlled data corruption for testing model robustness
"""

import pandas as pd
import numpy as np
from typing import Tuple

def poison_data(df: pd.DataFrame, poison_rate: float, random_state: int = 42) -> Tuple[pd.DataFrame, list]:
    """
    Poison dataset by randomly corrupting feature values
    
    Args:
        df: Original dataframe
        poison_rate: Percentage of data to poison (0.0 to 1.0)
        random_state: Random seed for reproducibility
        
    Returns:
        Tuple of (poisoned_df, poisoned_indices)
    """
    np.random.seed(random_state)
    df_poisoned = df.copy()
    
    # Calculate number of samples to poison
    n_samples = len(df)
    n_poison = int(n_samples * poison_rate)
    
    # Randomly select rows to poison
    poison_indices = np.random.choice(n_samples, n_poison, replace=False)
    
    # Feature columns (exclude target)
    feature_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    
    # Poison selected rows by adding random noise
    for idx in poison_indices:
        # Add random noise: uniform between -2 and +2 (significant corruption)
        noise = np.random.uniform(-2, 2, size=len(feature_cols))
        df_poisoned.loc[idx, feature_cols] += noise
        
        # Ensure values stay positive
        df_poisoned.loc[idx, feature_cols] = df_poisoned.loc[idx, feature_cols].clip(lower=0.1)
    
    print(f"✅ Poisoned {n_poison}/{n_samples} samples ({poison_rate*100:.0f}%)")
    print(f"   Poisoned indices: {sorted(poison_indices[:10])}...")
    
    return df_poisoned, list(poison_indices)


def create_poisoned_datasets(original_csv: str, poison_rates: list = [0.05, 0.10, 0.50]):
    """
    Create multiple poisoned versions of the dataset
    
    Args:
        original_csv: Path to original clean CSV
        poison_rates: List of poison rates to generate
        
    Returns:
        Dictionary of {rate: (poisoned_df, indices)}
    """
    # Load clean data
    df_clean = pd.read_csv(original_csv)
    print(f"📊 Loaded clean data: {len(df_clean)} samples\n")
    
    poisoned_datasets = {}
    
    for rate in poison_rates:
        print(f"🧪 Creating {rate*100:.0f}% poisoned dataset...")
        df_poison, indices = poison_data(df_clean, rate)
        
        # Save poisoned dataset
        output_path = f"data/poisoned/iris_poisoned_{int(rate*100)}pct.csv"
        df_poison.to_csv(output_path, index=False)
        print(f"   Saved to: {output_path}\n")
        
        poisoned_datasets[rate] = (df_poison, indices)
    
    return poisoned_datasets


def analyze_poisoning_impact(df_clean: pd.DataFrame, df_poisoned: pd.DataFrame):
    """
    Analyze statistical impact of poisoning
    
    Args:
        df_clean: Clean dataset
        df_poisoned: Poisoned dataset
    """
    feature_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    
    print("📈 Statistical Impact Analysis:")
    print("-" * 70)
    
    for col in feature_cols:
        clean_mean = df_clean[col].mean()
        poison_mean = df_poisoned[col].mean()
        clean_std = df_clean[col].std()
        poison_std = df_poisoned[col].std()
        
        mean_change = ((poison_mean - clean_mean) / clean_mean) * 100
        std_change = ((poison_std - clean_std) / clean_std) * 100
        
        print(f"{col:15s}: Mean {clean_mean:.2f}→{poison_mean:.2f} ({mean_change:+.1f}%), "
              f"Std {clean_std:.2f}→{poison_std:.2f} ({std_change:+.1f}%)")
    
    print("-" * 70)


if __name__ == "__main__":
    import os
    
    # Create poisoned data directory
    os.makedirs("data/poisoned", exist_ok=True)
    
    # Generate poisoned datasets
    datasets = create_poisoned_datasets("data/raw/iris.csv")
    
    print("\n✅ Data poisoning complete!")
