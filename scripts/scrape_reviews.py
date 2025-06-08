import pandas as pd
from google_play_scraper import reviews, Sort
from datetime import datetime
import os
import time

def scrape_reviews(app_id, bank_name, max_reviews=500):
    """Scrape up to max_reviews for a given app, keeping Amharic and emojis."""
    all_reviews = []
    count = 0
    batch_size = 100
    continuation_token = None

    while count < max_reviews:
        try:
            result, continuation_token = reviews(
                app_id,
                lang='en',  # still okay for multilingual – it doesn't block non-English
                country='us',
                sort=Sort.NEWEST,
                count=batch_size,
                filter_score_with=None,
                continuation_token=continuation_token
            )

            if not result:
                break

            for entry in result:
                all_reviews.append({
                    'review': entry.get('content', ''),
                    'rating': entry.get('score', None),
                    'date': entry.get('at'),
                    'bank': bank_name,
                    'source': 'Google Play'
                })

            count += len(result)

            # Prevent hammering the Play Store too fast
            time.sleep(1)

        except Exception as e:
            print(f"❌ Failed to fetch reviews for {bank_name}: {e}")
            break

        if continuation_token is None:
            break

    return pd.DataFrame(all_reviews)

def preprocess_dataframe(df):
    """Clean and preprocess review dataframe (preserve Amharic & emojis)."""
    df.drop_duplicates(subset=['review'], inplace=True)
    df.dropna(subset=['review', 'rating', 'date'], inplace=True)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    return df[['review', 'rating', 'date', 'bank', 'source']]

def main():
    # Verified app IDs
    apps = {
        "Commercial Bank of Ethiopia": "com.combanketh.mobilebanking",
        "Bank of Abyssinia": "com.boa.boaMobileBanking",
        "Dashen Bank": "com.dashen.dashensuperapp"
    }

    all_dfs = []

    for bank, app_id in apps.items():
        print(f"🔍 Scraping reviews for {bank}...")
        df = scrape_reviews(app_id, bank, max_reviews=500)
        if df.empty:
            print(f"⚠️ No reviews found for {bank}")
        else:
            df = preprocess_dataframe(df)
            print(f"✅ {len(df)} reviews collected for {bank}")
            all_dfs.append(df)

    if not all_dfs:
        print("❌ No data was collected for any app.")
        return

    full_df = pd.concat(all_dfs, ignore_index=True)

    # Get the current file's directory
    current_dir = os.path.dirname(__file__)

    # Construct the path relative to project root
    data_dir = os.path.join(current_dir, '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    output_path = os.path.join(data_dir, 'cleaned_reviews.csv')
    full_df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"✅ Saved cleaned reviews to {output_path}")
    print(f"🧾 Total reviews collected: {len(full_df)}")

if __name__ == "__main__":
    main()
