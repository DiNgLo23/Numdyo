from fastapi import APIRouter
from app.api.schemas import User, UserInDB, UpdateUsername, DeleteObj, GetUser, GetProblem
from app.db.crud import add_user, get_user, update_username, delete_user, get_problem
import time
router = APIRouter(prefix="/problem", tags=["problem"])



@router.get("/get_problem")
async def get_problem_end(problem_data:GetProblem):
    problem = get_problem(problem_data.id)
    return {"response":problem}