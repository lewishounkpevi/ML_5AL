import pandas as pd
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from data_processing import load_data, preprocess_data, prepare_train_test

def train_with_gridsearch(model, param_grid, X_train, y_train, X_test, y_test, label_encoder):
    grid = GridSearchCV(model, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_
    y_pred = best_model.predict(X_test)

    # Inverse transform des prédictions
    y_pred_labels = label_encoder.inverse_transform(y_pred)
    y_test_labels = label_encoder.inverse_transform(y_test)

    print(f"\n📊 {model.__class__.__name__} - GridSearchCV")
    print("✅ Meilleurs hyperparamètres :", grid.best_params_)
    print("✔️ Accuracy :", round(accuracy_score(y_test_labels, y_pred_labels), 4))
    print("📉 Matrice de confusion :\n", confusion_matrix(y_test_labels, y_pred_labels))
    print("📝 Rapport de classification :\n", classification_report(y_test_labels, y_pred_labels))

    return best_model, grid.best_params_, accuracy_score(y_test_labels, y_pred_labels)

if __name__ == "__main__":
    # Chargement et préparation
    df = load_data("data/raw_data/students_dataset.csv")
    preprocessor, X, y = preprocess_data(df)
    X_train, X_test, y_train, y_test, _ = prepare_train_test(preprocessor, X, y)

    # Encodage de la cible
    label_encoder = LabelEncoder()
    y_train_enc = label_encoder.fit_transform(y_train)
    y_test_enc = label_encoder.transform(y_test)

    # Sauvegarder preprocessor et label encoder
    joblib.dump(preprocessor, "app/models/preprocessor.joblib")
    joblib.dump(label_encoder, "app/models/label_encoder.joblib")
    print("✅ Preprocessor et label encoder sauvegardés")

    # Param grids
    param_grids = {
        "KNN": {"n_neighbors": [3, 5, 7]},
        "RandomForest": {"n_estimators": [100, 200], "max_depth": [None, 10, 20]},
        "XGBoost": {"n_estimators": [100, 200], "max_depth": [3, 5], "learning_rate": [0.1, 0.01]}
    }

    # Modèles
    models = {
        "KNN": KNeighborsClassifier(),
        "RandomForest": RandomForestClassifier(random_state=42),
        "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    }

    # Entraînement + sélection du meilleur
    best_model = None
    best_acc = 0
    best_name = ""
    best_params = {}

    for name in models:
        model, params, acc = train_with_gridsearch(
            models[name], param_grids[name], X_train, y_train_enc, X_test, y_test_enc, label_encoder
        )
        if acc > best_acc:
            best_acc = acc
            best_model = model
            best_name = name
            best_params = params

    # Sauvegarde du meilleur modèle
    joblib.dump(best_model, "app/model.joblib")
    print(f"\n🏆 Meilleur modèle : {best_name} ({round(best_acc, 4)}) ➜ model.joblib")
