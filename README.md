# fintech-mobile-banking-apps-analysis

This project involves scraping and analyzing Google Play Store reviews of three Ethiopian bank mobile apps: CBE, BOA, and Dashen Bank.

## Objective

To assist Omega Consultancy in identifying customer satisfaction drivers and pain points in order to help banks:

- Improve app features and performance
- Retain users and reduce churn
- Prioritize technical fixes and new features based on user feedback

## Task 1: Data Collection and Preprocessing

- Scraped 400+ reviews per bank
- Preprocessed data (cleaning, deduplication, date normalization)
- Stored in `data/cleaned_reviews.csv` and `data/processed_reviews.csv`

## Task 2: Sentiment and Thematic Analysis

- Stored in `thematic_analysis_output.csv`,`data/sentiment_aggregate_by_bank_rating.csv`and `data/reviews_with_sentimencsv`

## Task 3: Store Cleaned Data in Oracle

## Task 4: Insights and recommendations

## Methodology

1. Scraped reviews from Google Play for:
   - **CBE (Commercial Bank of Ethiopia)**
   - **BOA (Bank of Abyssinia)**
   - **Dashen Bank**
2. Saved raw reviews into: `data/raw_reviews.csv`
3. Preprocessed:
   - Removed duplicates and missing values
   - Converted date fields to `YYYY-MM-DD` format
4. Final cleaned dataset stored in: `data/clean_reviews.csv`  
   **Columns:**
   - `review`
   - `rating`
   - `date`
   - `bank`
   - `source`

## Tools & Technologies

- **Python**
- `google-play-scraper` – for collecting reviews
- **Pandas** – for data wrangling
- **Matplotlib, Seaborn** – for future visualizations
- **Jupyter Notebook** – for interactive analysis
- **Git & GitHub** – version control and collaboration

## Project Structure

fintech-mobile-banking-apps-analysis/
│
├── data/
│ ├── processed_reviews.csv
│ └── cleaned_reviews.csv
│ └── reviews_with_sentiment.csv
│ └── sentiment_aggregate_by_bank_rating.csv
│ └──thematic_analysis_output.csv
├── database/
│ └── bank_reviews_dump.sql
├── scripts/
│ └── scrape_reviews.py
│ └── preprocessing.py
│ └── sentiment_analysis.py
│ └── themantic_analysis.py
│ └── oracle_import_reviews.py
├── notebooks/
│ └── sentiment_analysis.ipynb
│ └── thematic_analysis_task4.ipynb
│ └── sentiment_analysis_from_oracle.ipynb
├── preprocessing.log
├── sentiment_analysis.log
├── requirements.txt
├── .gitignore
└── README.md
