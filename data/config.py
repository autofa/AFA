from pydantic import BaseModel

from data.problem import Problem
from datetime import datetime


class Config(BaseModel):
    name: str
    id: int
    contact: int
    email: str
    bank_id: int
    bank_name: str
    problem: Problem
    timestamp = datetime.strftime(datetime.now(), "%Y%m%d")

    @property
    def generated_name(self) -> str:
        return f"{self.problem.type}_{self.timestamp}_{self.problem.name}_{self.name}_{self.email}"
    
