# sentiment_analysis.py
import os
import pandas as pd
import logging
from pathlib import Path
from transformers import pipeline
from tqdm import tqdm

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sentiment_analysis.log'),
        logging.StreamHandler()
    ]
)

def load_processed_reviews(input_path):
    try:
        df = pd.read_csv(input_path, encoding='utf-8-sig')
        logging.info(f"Loaded processed reviews from {input_path}")
        return df
    except Exception as e:
        logging.error(f"Error loading processed reviews: {e}")
        return None

def apply_sentiment_analysis(df):
    logging.info("Loading sentiment analysis model...")
    sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    tqdm.pandas(desc="Analyzing Sentiment")

    def analyze(text):
        try:
            result = sentiment_model(text[:512])[0]  # Limit to 512 tokens
            return pd.Series([result['label'].lower(), result['score']])
        except Exception as e:
            logging.warning(f"Error processing text: {e}")
            return pd.Series(["neutral", 0.0])

    df[['sentiment_label', 'sentiment_score']] = df['review'].progress_apply(analyze)
    return df

def save_sentiment_output(df, output_path):
    try:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        logging.info(f"Saved sentiment-annotated reviews to {output_path}")
    except Exception as e:
        logging.error(f"Error saving sentiment file: {e}")

def main():
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, '..', 'data')

    input_path = os.path.join(data_dir, 'processed_reviews.csv')
    output_path = os.path.join(data_dir, 'reviews_with_sentiment.csv')

    logging.info("🔍 Starting sentiment analysis task...")

    df = load_processed_reviews(input_path)
    if df is None or df.empty:
        logging.error("No data to process. Exiting.")
        return

    df = apply_sentiment_analysis(df)
    save_sentiment_output(df, output_path)

    logging.info("✅ Sentiment analysis completed.")
    logging.info(f"Sample:\n{df[['review', 'sentiment_label', 'sentiment_score']].head()}")

    agg = df.groupby(['bank', 'rating'])['sentiment_score'].mean().reset_index()
    agg.to_csv("data/sentiment_aggregate_by_bank_rating.csv", index=False)


if __name__ == "__main__":
    main()
