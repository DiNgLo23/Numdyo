from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInDB(User):
    points: int
    level: int
    createAt: int
    updateAt: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None

class UpdateUsername(BaseModel):
    id: int
    new_username: str

class Problem(BaseModel):
    text: str
    answer: str
    level: int
    points: int

class ProblemWithVariant(BaseModel):
    text: str
    answer_a: str
    answer_b: str
    answer_c: str
    answer_d: str
    answer_true: str
    level: int
    points: int

class Achieve(BaseModel):
    title: str
    description: str
    picture: str

class DeleteObj(BaseModel):
    id: int

class GetUser(BaseModel):
    id: int

class GetProblem(BaseModel):
    id: int