import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
import os

def load_data(path='data/raw_data/students_dataset.csv'):
    return pd.read_csv(path)

def preprocess_data(df):
    if 'Student_ID' in df.columns:
        df = df.drop(columns=['Student_ID'])

    df = df[df['Status'].isin(['Success', 'Failure'])]

    X = df.drop(columns=['Status'])
    y = df['Status']

    numeric_features = X.select_dtypes(include='number').columns.tolist()
    categorical_features = X.select_dtypes(include='object').columns.tolist()

    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_pipeline, numeric_features),
        ("cat", categorical_pipeline, categorical_features)
    ])

    return preprocessor, X, y

def prepare_train_test(preprocessor, X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    return X_train_proc, X_test_proc, y_train, y_test, preprocessor

def save_processed_data(X_train_proc, X_test_proc, y_train, y_test, output_dir="data/processed_data"):
    os.makedirs(output_dir, exist_ok=True)

    # Convert to DataFrame if possible (X is numpy array after transform)
    pd.DataFrame(X_train_proc).to_csv(f"{output_dir}/X_train.csv", index=False)
    pd.DataFrame(X_test_proc).to_csv(f"{output_dir}/X_test.csv", index=False)
    y_train.to_csv(f"{output_dir}/y_train.csv", index=False)
    y_test.to_csv(f"{output_dir}/y_test.csv", index=False)

    print(f"💾 Données sauvegardées dans {output_dir}/")

if __name__ == "__main__":
    df = load_data("data/raw_data/students_dataset.csv")
    preprocessor, X, y = preprocess_data(df)
    X_train, X_test, y_train, y_test, prep = prepare_train_test(preprocessor, X, y)

    save_processed_data(X_train, X_test, y_train, y_test)
    print(f"✅ Données prêtes : {X_train.shape[0]} lignes d'entraînement, {X_test.shape[0]} lignes de test.")
