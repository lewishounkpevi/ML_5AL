from pydantic import BaseModel

class StudentInput(BaseModel):
    age: int
    student_income: float
    parent_income: float
    academic_year: int
    region: str
    residence_type: str
    gender: str
    grade_math: float
    grade_programming: float
    grade_algorithms: float
    grade_databases: float
    grade_software_engineering: float


class PredictionOutput(BaseModel):
    prediction: str
    probability: float

class ClusteringInput(BaseModel):
    grade_math: float
    grade_programming: float
    grade_algorithms: float
    grade_databases: float
    grade_software_engineering: float

class ClusteringOutput(BaseModel):
    cluster: int | None