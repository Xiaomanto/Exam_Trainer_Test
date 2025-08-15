from pydantic import BaseModel

class Exam(BaseModel):
    ques: str
    answer:str
    optionA:str
    optionB:str
    optionC:str
    optionD:str
    description:str

    @classmethod
    def from_json(cls, data:dict):
        return cls(**data)

class UserAns(BaseModel):
    id: int
    ans:str
    current_ans:str
    is_correct:bool