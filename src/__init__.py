# Importation des fonctions de connexion à différentes bases de données
from .generate_data import (
    generate_student_dataset,
    generate_dirty_student_dataset,
    clean_student_dataset,
)


from .utils import (
    notify_done,
)

from .predict import predict_student_status

from .model_training import train_with_gridsearch

from .data_processing import load_data, preprocess_data, prepare_train_test

# Optionnellement, définir __all__ pour limiter ce que 'import *' va inclure
__all__ = [
    'generate_student_dataset',
    'generate_dirty_student_dataset',
    'clean_student_dataset',
    'predict_student_status',
    'notify_done',
    'train_with_gridsearch',
    'load_data', 
    'preprocess_data', 
    'prepare_train_test',
]
