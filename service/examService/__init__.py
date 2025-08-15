from typing_extensions import Literal
from Component import Exam, UserAns
import random as r
import json

class ExamService:
    def __init__(self) -> None:
        self.ExamQues:list[Exam] | None = None
        self.reset()
        return

    def load_exam(self, path:str) -> None:
        with open(path,'r',encoding='utf-8') as f:
            self.ExamQues = [Exam.from_json(x) for x in json.load(f)]

    def set_Ramdom_Ques(self, limit:Literal['all','25','50']='all') -> None:
        if self.ExamQues is None:
            raise Exception('請先加載題庫！！')
        if limit == 'all':
            self.Ramdom = self.ExamQues[:]
            return
        if limit == '25':
            r.shuffle(self.ExamQues)
            self.Ramdom = self.ExamQues[:25]
            return
        if limit == '50':
            r.shuffle(self.ExamQues)
            self.Ramdom = self.ExamQues[:50]
            return
        
    def reset(self) -> None:
        self.userAns:list[UserAns] | None = []
        self.score:int = 0
        self.Ramdom:list[Exam] | None = None
        return
    
    def set_ans(self,id:int,userAns:str) -> None:
        if self.Ramdom is None:
            raise Exception('請先選擇題數！！')
        try:
            self.userAns[id].ans = userAns
            self.userAns[id].is_correct = userAns == self.Ramdom[id].answer
        except Exception as e:    
            self.userAns.append(
                UserAns(
                    id=id,
                    ans=userAns,
                    current_ans=self.Ramdom[id].answer,
                    is_correct=userAns == self.Ramdom[id].answer
                )
            )
    
    def get_score(self) -> float:
        if self.Ramdom is None:
            raise Exception('請先選擇題數！！')
        if self.userAns is None:
            return 0.0
        for i in self.userAns:
            if i.is_correct:
                self.score += 1
        return self.score/len(self.userAns)*100