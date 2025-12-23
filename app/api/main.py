from fastapi import FastAPI
#from app.db.models import create_table_problems,create_table_users,create_table_achievement
from app.api.routers import users, achievement, problems
import uvicorn
app = FastAPI()


app.include_router(users.router)
app.include_router(achievement.router)
app.include_router(problems.router)




@app.get("/")
def read_root():
    return {"message": "None"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)