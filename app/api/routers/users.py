from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.api.schemas import User, UserInDB, UpdateUsername, DeleteObj, GetUser, UserLogin, Token
from app.db.crud import (
    add_user, get_user, update_username, delete_user,
    authenticate_user, create_access_token, verify_token, get_user_by_id
)
from datetime import timedelta
import time

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user


@router.post("/add_user")
async def add_user_end(user_data: User):
    user_data = UserInDB(
        **user_data.dict(),
        points=0,
        level=0,
        createAt=int(time.time()),
        updateAt=int(time.time())
    )
    add_user(user_data)
    return {"response": 200, "message": "User created successfully"}


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(user["id"]), "email": user["email"]},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):

    current_user.pop("password", None)
    return current_user


@router.patch("/change_username")
async def change_username_end(
        update_username_data: UpdateUsername,
        current_user: dict = Depends(get_current_user)
):

    if current_user["id"] != update_username_data.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to change this username"
        )

    success = update_username(update_username_data.id, update_username_data.new_username)
    if success:
        return {"response": 200, "message": "Username updated successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


@router.delete("/delete_user")
async def delete_user_end(
        delete_user_data: DeleteObj,
        current_user: dict = Depends(get_current_user)
):

    if current_user["id"] != delete_user_data.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )

    if get_user(delete_user_data.id):
        delete_user(delete_user_data.id)
        return {"response": 200, "message": "User deleted successfully"}
    else:
        return {"response": 404, "message": "User not found"}