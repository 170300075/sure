from pydantic import BaseModel

class SelectedSubject(BaseModel):
    section : float
    id_subject : str

class Predictors(BaseModel):
    recursada : float
    tasa_rep_carga : float
    ceneval_analitico : float
    ceneval_matematico : float
    prom_per_prev : float
    asigMuchas : float
    complejidad_carga5 : float
    situacion_irregular : float