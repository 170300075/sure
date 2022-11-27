from pydantic import BaseModel

class SubjectGrade(BaseModel):
    number : int
    type : str
    section : int
    id_subject : str
    teacher : str
    modality : str
    subject : str
    first_partial : float | str
    second_partial : float | str
    third_partial : float | str
    average : float | str
    final_grade : float | str
    period : int
    id_user : str