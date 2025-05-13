import pandas as pd
import os
import tempfile
from src.data_processing import preprocess_data, prepare_train_test
from src.generate_data import generate_student_dataset
from src.model_training import train_with_gridsearch
from src.clustering_training import train_kmeans_with_silhouette, fit_cluster_model
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier


def generate_df(n=1000, years=5):
    tmp_dir = tempfile.mkdtemp()
    tmp_path = os.path.join(tmp_dir, "students.csv")
    generate_student_dataset(n_students=n, n_years=years, output_csv=tmp_path)
    return pd.read_csv(tmp_path)


def test_data_pipeline():
    df = generate_df()
    preprocessor, X, y = preprocess_data(df)
    X_train, X_test, y_train, y_test, prep = prepare_train_test(preprocessor, X, y)

    assert X_train.shape[0] > 0
    assert X_train.shape[1] == X_test.shape[1]
    assert len(y_train) == X_train.shape[0]


def test_model_training():
    df = generate_df()
    preprocessor, X, y = preprocess_data(df)
    X_train, X_test, y_train, y_test, prep = prepare_train_test(preprocessor, X, y)

    label_encoder = LabelEncoder()
    y_train_enc = label_encoder.fit_transform(y_train)
    y_test_enc = label_encoder.transform(y_test)

    model = RandomForestClassifier(random_state=42)
    param_grid = {"n_estimators": [10], "max_depth": [None]}

    best_model, best_params, acc = train_with_gridsearch(
        model, param_grid, X_train, y_train_enc, X_test, y_test_enc, label_encoder
    )

    assert acc >= 0 and acc <= 1
    assert hasattr(best_model, "predict")


def test_train_kmeans_with_silhouette():
    os.makedirs(os.path.join(tempfile.gettempdir(), "models"), exist_ok=True)
    df = generate_df(n=200, years=2)
    tmp_dir = tempfile.mkdtemp()
    tmp_file = os.path.join(tmp_dir, "sample.csv")
    df.to_csv(tmp_file, index=False)

    os.makedirs(os.path.join(tmp_dir, "models"), exist_ok=True)
    train_kmeans_with_silhouette(tmp_file, save_path=tmp_dir)

    model_path = os.path.join(tmp_dir, "models/cluster_model.joblib")
    scaler_path = os.path.join(tmp_dir, "models/cluster_scaler.joblib")

    assert os.path.exists(model_path)
    assert os.path.exists(scaler_path)


def test_fit_cluster_model():
    df = generate_df()
    grade_cols = [
        "Grade_Math",
        "Grade_Programming",
        "Grade_Algorithms",
        "Grade_Databases",
        "Grade_Software_Engineering",
    ]
    df = df.dropna(subset=grade_cols)
    model, labels, score = fit_cluster_model(df[grade_cols], k_range=(2, 4))

    assert len(labels) == df.shape[0]
    assert 0 <= score <= 1
    assert hasattr(model, "predict")
