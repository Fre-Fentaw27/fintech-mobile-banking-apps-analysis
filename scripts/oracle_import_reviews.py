import cx_Oracle
import pandas as pd
from pathlib import Path

# Set the path to your Oracle client (if needed)
# cx_Oracle.init_oracle_client(lib_dir=r"your_oracle_client_path")

# Database connection details
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XEPDB1")
connection = cx_Oracle.connect(user="bank_review", password="DB12345", dsn=dsn)

# Path to your CSV file
csv_path = Path('../data/processed_reviews.csv') 

# Read CSV file
df = pd.read_csv(csv_path)

# Clean data if needed (handle missing values, format dates, etc.)
df['date'] = pd.to_datetime(df['date']).dt.date

# Get unique banks
unique_banks = df['bank'].unique()

# Insert banks and create mapping
bank_id_map = {}
with connection.cursor() as cursor:
    # Insert banks
    for bank_name in unique_banks:
        bank_id_var = cursor.var(cx_Oracle.NUMBER)
        cursor.execute("""
            INSERT INTO banks (bank_name) 
            VALUES (:1) 
            RETURNING bank_id INTO :2
        """, [bank_name, bank_id_var])
        bank_id = bank_id_var.getvalue()[0]
        bank_id_map[bank_name] = bank_id
    
    connection.commit()
    
    # Prepare review data
    review_data = []
    for _, row in df.iterrows():
        review_data.append({
            'bank_id': bank_id_map[row['bank']],
            'review_text': row['review'],
            'rating': row['rating'],
            'review_date': row['date'],
            'source': row['source']
        })
    
    # Batch insert reviews
    cursor.executemany("""
        INSERT INTO reviews (bank_id, review_text, rating, review_date, source)
        VALUES (:bank_id, :review_text, :rating, :review_date, :source)
    """, review_data)
    
    connection.commit()
print(f"Inserted {len(unique_banks)} banks and {len(df)} reviews")
connection.close()