
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    classification_report, confusion_matrix,
    ConfusionMatrixDisplay, precision_score, recall_score, f1_score
)
import matplotlib.pyplot as plt
import joblib

os.chdir(r'C:\Users\DELL\misinformation-detector')
os.makedirs('model', exist_ok=True)

# ── Load Data ──────────────────────────────────────────────
fake = pd.read_csv('data/Fake.csv')
real = pd.read_csv('data/True.csv')

fake['label'] = 0
real['label'] = 1

df = pd.concat([fake, real], ignore_index=True)
df = df[['title', 'label']].dropna()
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"Dataset size: {len(df)} headlines")
print(f"Fake: {len(df[df.label==0])} | Real: {len(df[df.label==1])}")

# ── Split ──────────────────────────────────────────────────
X = df['title']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train: {len(X_train)} | Test: {len(X_test)}")

# ── Pipeline ───────────────────────────────────────────────
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=10000,
        min_df=2
    )),
    ('clf', LogisticRegression(
        C=1.0,
        max_iter=1000,
        random_state=42
    ))
])

# ── Train ──────────────────────────────────────────────────
print("\nTraining model...")
pipeline.fit(X_train, y_train)
print("Done!")

# ── Evaluate ───────────────────────────────────────────────
y_pred = pipeline.predict(X_test)
y_prob = pipeline.predict_proba(X_test)[:, 1]

print("\n── Classification Report ──")
print(classification_report(y_test, y_pred, target_names=['Fake','Real']))

print(f"Precision : {precision_score(y_test, y_pred):.4f}")
print(f"Recall    : {recall_score(y_test, y_pred):.4f}")
print(f"F1 Score  : {f1_score(y_test, y_pred):.4f}")

# ── Confusion Matrix ───────────────────────────────────────
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(cm, display_labels=['Fake','Real'])
disp.plot(cmap='Blues')
plt.title('Confusion Matrix')
plt.savefig('model/confusion_matrix.png')
print("Confusion matrix saved to model/confusion_matrix.png")

# ── Save Model ─────────────────────────────────────────────
joblib.dump(pipeline, 'model/pipeline.pkl')
print("Model saved to model/pipeline.pkl ✅")
