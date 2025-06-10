import oracledb as cx_Oracle  # if you want backward compatibility
import pandas as pd
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Database connection details
DB_USER = os.getenv('ORACLE_USER')
DB_PASSWORD = os.getenv('ORACLE_PASSWORD')
DSN = os.getenv('ORACLE_DSN')  # e.g., "localhost:1521/XE"

def get_db_connection():
    try:
        connection = cx_Oracle.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DSN
        )
        print("Successfully connected to Oracle Database")
        return connection
    except cx_Oracle.DatabaseError as e:
        print(f"Database connection failed: {e}")
        raise

def insert_banks(connection, bank_names):
    cursor = connection.cursor()
    try:
        # Only insert banks that don't exist
        cursor.execute("SELECT bank_name FROM banks")
        existing_banks = [row[0] for row in cursor]
        
        new_banks = [b for b in bank_names if b not in existing_banks]
        
        for bank_name in new_banks:
            cursor.execute(
                "INSERT INTO banks (bank_id, bank_name) VALUES (bank_seq.NEXTVAL, :1)",
                [bank_name]
            )
        connection.commit()
        print(f"Inserted {len(new_banks)} new banks")
    except cx_Oracle.DatabaseError as e:
        connection.rollback()
        print(f"Error inserting banks: {e}")
        raise

def insert_reviews(connection, df):
    cursor = connection.cursor()
    try:
        # Get bank_id mapping
        cursor.execute("SELECT bank_id, bank_name FROM banks")
        bank_id_map = {name: id for id, name in cursor}
        
        # Prepare batch insert data
        batch_data = []
        for _, row in df.iterrows():
            batch_data.append({
                'bank_id': bank_id_map[row['bank']],
                'review_text': str(row['review']),
                'rating': float(row['rating']) if pd.notna(row['rating']) else None,
                'review_date': datetime.strptime(row['date'], '%Y-%m-%d').date() if pd.notna(row['date']) else None,
                'source': str(row['source']) if pd.notna(row['source']) else 'Unknown'
            })
        
        # Execute batch insert
        cursor.executemany(
            """
            INSERT INTO reviews (
                review_id, bank_id, review_text, rating, 
                review_date, source
            ) VALUES (
                review_seq.NEXTVAL, :bank_id, :review_text, :rating,
                :review_date, :source
            )
            """,
            batch_data
        )
        connection.commit()
        print(f"Successfully inserted {len(df)} reviews")
        
    except cx_Oracle.DatabaseError as e:
        connection.rollback()
        print(f"Error inserting reviews: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def main():
    # Load the processed reviews data
    csv_path = '../data/processed_reviews.csv'
    reviews_df = pd.read_csv(csv_path)
    
    # Clean data - handle missing values
    reviews_df['bank'] = reviews_df['bank'].fillna('Unknown')
    reviews_df['source'] = reviews_df['source'].fillna('Unknown')
    reviews_df['review'] = reviews_df['review'].fillna('')
    
    # Get unique bank names
    bank_names = reviews_df['bank'].unique()
    
    try:
        connection = get_db_connection()
        
        # Insert banks first
        insert_banks(connection, bank_names)
        
        # Insert reviews
        insert_reviews(connection, reviews_df)
        
        # Verification counts
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM banks")
        print(f"Total banks in database: {cursor.fetchone()[0]}")
        cursor.execute("SELECT COUNT(*) FROM reviews")
        print(f"Total reviews in database: {cursor.fetchone()[0]}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    main()