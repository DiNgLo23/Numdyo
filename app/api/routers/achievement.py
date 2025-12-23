from fastapi import APIRouter
from app.api.schemas import DeleteObj, Achieve, DeleteObj
from app.db.crud import add_achievement, delete_achievement


router = APIRouter(prefix="/achievement", tags=["achievement"])


@router.post("/add_achievement")
async def add_achievement_end(achievement_data:Achieve):
    add_achievement(achievement_data)
    return {"response":200}



@router.delete("/delete_achievement")
async def delete_achievement_end(achievement_data:DeleteObj):
    delete_achievement(achievement_data.id)
    return {"response":200}

