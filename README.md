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
│
├── scripts/
│ └── scrape_reviews.py
│ └── preprocessing.py
│
├── notebooks/
│ └── sentiment_analysis.ipynb
│ └── thematic_analysis.ipynb
├── preprocessing.log
├── requirements.txt
├── .gitignore
└── README.md
