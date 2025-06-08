import pandas as pd
import numpy as np
from datetime import datetime
import os
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('preprocessing.log'),
        logging.StreamHandler()
    ]
)

def load_data(input_path):
    """Load the scraped reviews data"""
    try:
        df = pd.read_csv(input_path, encoding='utf-8-sig')
        logging.info(f"Successfully loaded data from {input_path}")
        logging.info(f"Initial shape: {df.shape}")
        return df
    except Exception as e:
        logging.error(f"Failed to load data: {str(e)}")
        return None

def remove_duplicates(df):
    """Remove duplicate reviews while preserving Amharic text and emojis"""
    # Case-insensitive deduplication
    df['review_lower'] = df['review'].str.lower()
    initial_count = len(df)
    df = df.drop_duplicates(subset=['review_lower'], keep='first')
    df = df.drop(columns=['review_lower'])
    removed = initial_count - len(df)
    logging.info(f"Removed {removed} duplicate reviews")
    return df

def handle_missing_data(df):
    """Clean and impute missing values"""
    # Drop rows with missing reviews
    initial_count = len(df)
    df = df.dropna(subset=['review'])
    
    # Fill missing ratings with 0 and convert to integer
    df['rating'] = df['rating'].fillna(0).astype(int)
    
    # Ensure ratings are between 1-5
    df['rating'] = np.where(df['rating'] < 1, 1, df['rating'])
    df['rating'] = np.where(df['rating'] > 5, 5, df['rating'])
    
    removed = initial_count - len(df)
    logging.info(f"Removed {removed} rows with missing data")
    return df

def normalize_dates(df):
    """Convert dates to standardized YYYY-MM-DD format"""
    try:
        # Convert to datetime and handle invalid dates
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Drop rows with invalid dates
        initial_count = len(df)
        df = df.dropna(subset=['date'])
        removed = initial_count - len(df)
        
        # Format dates
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        
        logging.info(f"Normalized dates, removed {removed} invalid entries")
        return df
    except Exception as e:
        logging.error(f"Date normalization failed: {str(e)}")
        return df

def save_processed_data(df, output_path):
    """Save the processed data with proper encoding"""
    try:
        # Ensure output directory exists
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save with UTF-8-SIG encoding to preserve Amharic and emojis
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        logging.info(f"Successfully saved processed data to {output_path}")
        return True
    except Exception as e:
        logging.error(f"Failed to save data: {str(e)}")
        return False

def main():
    # Get the current file's directory (e.g., scripts/)
    current_dir = os.path.dirname(__file__)

    # Resolve path to project root (one level up)
    project_root = os.path.abspath(os.path.join(current_dir, '..'))

    # Construct the full paths inside the project root's data folder
    data_dir = os.path.join(project_root, 'data')
    input_path = os.path.join(data_dir, 'cleaned_reviews.csv')
    output_path = os.path.join(data_dir, 'processed_reviews.csv')
    
    logging.info("Starting preprocessing pipeline")
    
    # 1. Load data
    df = load_data(input_path)
    if df is None:
        return
    
    # 2. Remove duplicates
    df = remove_duplicates(df)
    
    # 3. Handle missing data
    df = handle_missing_data(df)
    
    # 4. Normalize dates
    df = normalize_dates(df)
    
    # 5. Select and order columns
    final_columns = ['review', 'rating', 'date', 'bank', 'source']
    df = df[final_columns]
    
    # 6. Save processed data
    if save_processed_data(df, output_path):
        logging.info("\n=== Preprocessing Summary ===")
        logging.info(f"Final dataset shape: {df.shape}")
        logging.info(f"Total reviews processed: {len(df)}")
        logging.info("\nSample of processed data:")
        logging.info(df.head(3).to_string())

if __name__ == "__main__":
    main()