import pandas as pd
import re
import spacy
from tqdm import tqdm
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")
tqdm.pandas()

# ----------------- Preprocessing ------------------
def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
    return " ".join(tokens)

# ----------------- Keyword Extraction ------------------
def extract_keywords(texts, top_n=5):
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(texts)
    features = vectorizer.get_feature_names_out()
    
    top_keywords = []
    for row in X:
        indices = row.toarray().flatten().argsort()[-top_n:][::-1]
        keywords = [features[i] for i in indices]
        top_keywords.append(keywords)
    return top_keywords

# ----------------- Rule-based Thematic Clustering ------------------
def assign_theme(keywords):
    theme_map = {
        "login": "Account Access",
        "password": "Account Access",
        "transfer": "Transaction Performance",
        "delay": "Transaction Performance",
        "crash": "App Reliability",
        "support": "Customer Support",
        "help": "Customer Support",
        "interface": "User Experience",
        "design": "User Experience",
        "feature": "Feature Request",
    }

    themes = set()
    for word in keywords:
        for key, theme in theme_map.items():
            if key in word:
                themes.add(theme)
    return list(themes) if themes else ["Miscellaneous"]

# ----------------- Main Pipeline ------------------
if __name__ == "__main__":
    # 1. Load data
    df = pd.read_csv("data/processed_reviews.csv")

    # 2. Preprocess reviews
    df["clean_review"] = df["review"].progress_apply(preprocess)

    # 3. Extract keywords
    df["keywords"] = extract_keywords(df["clean_review"].tolist())

    # 4. Assign themes
    df["themes"] = df["keywords"].apply(assign_theme)

    # 5. Save output
    output_df = df[["review", "rating", "date", "bank", "source", "keywords", "themes"]]
    output_df.to_csv("data/thematic_analysis_output.csv", index=False)

    print("✅ Thematic analysis completed and saved to data/thematic_analysis_output.csv")

