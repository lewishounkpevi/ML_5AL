import pandas as pd
import numpy as np
import random

def generate_student_dataset(n_students=50000, n_years=20, start_year=2005, output_csv='students_dataset.csv'):
    """
    Génère un fichier CSV simulant des étudiants en école de software ingénieur.

    Paramètres :
    - n_students : nombre d'étudiants à générer
    - n_years : nombre d'années académiques (réparties de manière aléatoire)
    - start_year : année de départ pour les années académiques
    - output_csv : nom du fichier de sortie CSV
    """

    np.random.seed(42)
    random.seed(42)

    # Génération des données de base
    student_id = np.arange(1, n_students + 1)
    age = np.random.randint(18, 30, size=n_students)
    gender = np.random.choice(['Male', 'Female', 'Other'], size=n_students, p=[0.48, 0.48, 0.04])

    # Notes de cours
    course_names = ['Math', 'Programming', 'Algorithms', 'Databases', 'Software_Engineering']
    grades = {
        course: np.round(np.random.normal(12, 3, size=n_students), 1)
        for course in course_names
    }

    # Revenus étudiants et parents
    student_income = np.round(np.random.normal(600, 250, size=n_students))
    student_income = np.clip(student_income, 0, None)

    parent_income = np.round(np.random.normal(2500, 800, size=n_students))
    parent_income = np.clip(parent_income, 500, None)

    # Localisation
    urban_rural = np.random.choice(['Urban', 'Suburban', 'Rural'], size=n_students, p=[0.5, 0.3, 0.2])
    region = np.random.choice(
        ['Île-de-France', 'Auvergne-Rhône-Alpes', 'Nouvelle-Aquitaine', 'Occitanie', 'Grand Est', 'Hauts-de-France'],
        size=n_students
    )

    # Année académique
    years_range = list(range(start_year, start_year + n_years))
    academic_year = np.random.choice(years_range, size=n_students)

    # Moyenne générale & réussite
    average_grade = np.round(np.mean([grades[c] for c in course_names], axis=0), 2)
    status = np.where(average_grade >= 10, 'Success', 'Failure')

    # Création du DataFrame
    df = pd.DataFrame({
        'Student_ID': student_id,
        'Age': age,
        'Gender': gender,
        'Student_Income_EUR': student_income,
        'Parent_Income_EUR': parent_income,
        'Residence_Type': urban_rural,
        'Region': region,
        'Academic_Year': academic_year,
        'Average_Grade': average_grade,
        'Status': status
    })

    for course in course_names:
        df[f'Grade_{course}'] = grades[course]

    # Export CSV
    df.to_csv(output_csv, index=False)
    print(f"✅ Fichier '{output_csv}' généré avec {n_students} lignes sur {n_years} années.")

# Exemple d'utilisation :
# generate_student_dataset(n_students=10000, n_years=10, output_csv="students_10k_10years.csv")

import pandas as pd
import numpy as np
import random

def generate_dirty_student_dataset(n_students=50000, n_years=20, start_year=2005, output_csv='dirty_students_dataset.csv'):
    """
    Génère un jeu de données "sale" simulant des étudiants en école d'ingénieur logiciel.
    Contient des erreurs classiques de données : valeurs manquantes, doublons, fautes, recodages...
    """

    np.random.seed(42)
    random.seed(42)

    # Données de base
    student_id = np.arange(1, n_students + 1)
    age = np.random.randint(18, 30, size=n_students)
    gender = np.random.choice(['Male', 'FEMALE', 'femle', 'male', 'Other', 'F'], size=n_students,
                              p=[0.3, 0.2, 0.1, 0.1, 0.1, 0.2])
    
    course_names = ['Math', 'Programming', 'Algorithms', 'Databases', 'Software_Engineering']
    grades = {
        course: np.round(np.random.normal(12, 3, size=n_students), 1)
        for course in course_names
    }

    student_income = np.round(np.random.normal(600, 250, size=n_students))
    student_income = np.clip(student_income, 0, None)

    parent_income = np.round(np.random.normal(2500, 800, size=n_students))
    parent_income = np.clip(parent_income, 500, None)

    urban_rural = np.random.choice(['Urban', 'Suburban', 'rural', 'URBAN', 'Rural'], size=n_students,
                                   p=[0.4, 0.25, 0.15, 0.1, 0.1])
    
    region = np.random.choice(
        ['Île-de-France', 'AUVERGNE-RHONE-ALPES', 'nouvelle-aquitaine', 'Occitanie', 'GrandEst', 'Hauts-de-france'],
        size=n_students
    )

    years_range = list(range(start_year, start_year + n_years))
    academic_year = np.random.choice(years_range, size=n_students)

    average_grade = np.round(np.mean([grades[c] for c in course_names], axis=0), 2)
    status = np.where(average_grade >= 10, 'Success', 'failure')

    # Création DataFrame
    df = pd.DataFrame({
        'Student_ID': student_id,
        'Age': age,
        'Gender': gender,
        'Student_Income': student_income,
        'Parent_Income': parent_income,
        'Residence': urban_rural,
        'Region': region,
        'Academic_Year': academic_year,
        'Average_Grade': average_grade,
        'Status': status
    })

    for course in course_names:
        df[f'Grade_{course}'] = grades[course]

    # Injecter du bruit et des problèmes
    # 1. Valeurs manquantes (NaN)
    for col in ['Age', 'Gender', 'Parent_Income', 'Region', 'Grade_Math']:
        missing_indices = np.random.choice(df.index, size=int(0.05 * n_students), replace=False)
        df.loc[missing_indices, col] = np.nan

    # 2. Doublons
    duplicate_rows = df.sample(frac=0.01, random_state=1)
    df = pd.concat([df, duplicate_rows], ignore_index=True)

    # 3. Champs inutiles ou bruités
    df['Notes'] = np.random.choice(['bon', 'moyen', 'null', np.nan], size=len(df), p=[0.2, 0.3, 0.3, 0.2])
    df['Extra_Column'] = 'TO_REMOVE'

    # 4. Incohérence dans le statut (moyenne < 10 mais statut "Success")
    flip_indices = df[df['Average_Grade'] < 10].sample(frac=0.1).index
    df.loc[flip_indices, 'Status'] = 'Success'

    # Sauvegarde
    df.to_csv(output_csv, index=False)
    print(f"⚠️ Fichier sale '{output_csv}' généré avec {len(df)} lignes (avec bruit, doublons et valeurs manquantes).")

# Exemple d'appel :
# generate_dirty_student_dataset(n_students=10000, n_years=5, output_csv="dirty_students.csv")


import pandas as pd
import numpy as np

def clean_student_dataset(input_csv='dirty_students_dataset.csv', output_csv='cleaned_students_dataset.csv'):
    """
    Nettoie le dataset d'étudiants : doublons, valeurs manquantes, recodage, nettoyage des incohérences.
    """

    df = pd.read_csv(input_csv)

    print(f"🔍 Dataset brut : {df.shape[0]} lignes, {df.shape[1]} colonnes")

    # 1. Supprimer les colonnes inutiles
    if 'Extra_Column' in df.columns:
        df.drop(columns=['Extra_Column'], inplace=True)

    # 2. Supprimer les doublons
    df.drop_duplicates(inplace=True)

    # 3. Traiter les valeurs manquantes
    df['Age'].fillna(df['Age'].median(), inplace=True)
    df['Parent_Income'].fillna(df['Parent_Income'].median(), inplace=True)
    df['Gender'].fillna('Unknown', inplace=True)
    df['Region'].fillna('Unknown', inplace=True)
    df['Grade_Math'].fillna(df['Grade_Math'].mean(), inplace=True)
    df['Notes'].fillna('non précisé', inplace=True)

    # 4. Nettoyer et recoder les variables catégorielles
    df['Gender'] = df['Gender'].str.lower().map({
        'male': 'Male', 'female': 'Female', 'femle': 'Female',
        'f': 'Female', 'other': 'Other', 'unknown': 'Unknown'
    })

    df['Residence'] = df['Residence'].str.lower().map({
        'urban': 'Urban', 'suburban': 'Suburban', 'rural': 'Rural'
    })

    df['Region'] = df['Region'].str.title().str.replace('-', ' ')
    df['Status'] = df['Status'].str.capitalize()

    # 5. Recalculer les moyennes et corriger les incohérences de statut
    grade_columns = [col for col in df.columns if col.startswith('Grade_')]
    df['Average_Grade_Corrected'] = df[grade_columns].mean(axis=1).round(2)
    df['Status'] = np.where(df['Average_Grade_Corrected'] >= 10, 'Success', 'Failure')

    # 6. Réorganiser les colonnes
    columns_order = [
        'Student_ID', 'Age', 'Gender', 'Student_Income', 'Parent_Income',
        'Residence', 'Region', 'Academic_Year'
    ] + grade_columns + ['Average_Grade_Corrected', 'Status', 'Notes']

    df = df[columns_order]

    # 7. Sauvegarde du fichier propre
    df.to_csv(output_csv, index=False)
    print(f"✅ Dataset nettoyé sauvegardé dans '{output_csv}' ({df.shape[0]} lignes).")

# Exemple d'utilisation :
# clean_student_dataset('dirty_students_dataset.csv', 'cleaned_students_dataset.csv')
