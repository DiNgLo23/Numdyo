import sqlite3
from app.api.schemas import User, Problem, Achieve
import time
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional


SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email: str, password: str) -> Optional[dict]:
    con = sqlite3.connect("../../data/NumDuo.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
    user_data = cursor.fetchone()
    con.close()

    if not user_data:
        return None

    columns = ['id', 'username', 'email', 'password', 'points', 'level', 'createAt', 'updateAt']
    user_dict = dict(zip(columns, user_data))

    if not verify_password(password, user_dict['password']):
        return None

    return user_dict


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    try:
        import jwt
    except ImportError:
        import base64
        import json
        import hashlib
        import hmac

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire.timestamp()})

        header = json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
        payload = json.dumps(to_encode).encode()

        header_b64 = base64.urlsafe_b64encode(header).decode().rstrip('=')
        payload_b64 = base64.urlsafe_b64encode(payload).decode().rstrip('=')

        signature = hmac.new(
            SECRET_KEY.encode(),
            f"{header_b64}.{payload_b64}".encode(),
            hashlib.sha256
        ).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')

        return f"{header_b64}.{payload_b64}.{signature_b64}"
    else:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    try:
        import jwt
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.InvalidTokenError:
            return None
    except ImportError:
        try:
            import base64
            import json
            import hashlib
            import hmac

            parts = token.split('.')
            if len(parts) != 3:
                return None

            header_b64, payload_b64, signature_b64 = parts


            padding = 4 - len(header_b64) % 4
            if padding < 4:
                header_b64 += '=' * padding

            padding = 4 - len(payload_b64) % 4
            if padding < 4:
                payload_b64 += '=' * padding


            message = f"{parts[0]}.{parts[1]}"
            expected_signature = hmac.new(
                SECRET_KEY.encode(),
                message.encode(),
                hashlib.sha256
            ).digest()
            expected_signature_b64 = base64.urlsafe_b64encode(expected_signature).decode().rstrip('=')

            if signature_b64 != expected_signature_b64:
                return None

            payload_json = base64.urlsafe_b64decode(payload_b64).decode()
            payload = json.loads(payload_json)


            if 'exp' in payload:
                if datetime.utcnow().timestamp() > payload['exp']:
                    return None

            return payload
        except:
            return None


def get_user_by_id(user_id: int) -> Optional[dict]:
    con = sqlite3.connect("../../data/NumDuo.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    con.close()

    if not user_data:
        return None

    columns = ['id', 'username', 'email', 'password', 'points', 'level', 'createAt', 'updateAt']
    return dict(zip(columns, user_data))




def add_user(user_data: User):
    con = sqlite3.connect("../../data/NumDuo.db")
    cursor = con.cursor()
    cursor.execute(f"""
                            INSERT INTO Users (username, email, password, points, level, createAt, updateAt)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
        user_data.username,
        user_data.email,
        get_password_hash(user_data.password),
        user_data.points,
        user_data.level,
        user_data.createAt,
        user_data.updateAt
    ))
    con.commit()
    con.close()


def add_problem(problem_data: Problem):
    con = sqlite3.connect("../../data/NumDuo.db")
    cursor = con.cursor()
    cursor.execute("""
                            INSERT INTO Problems (id, text, answer, level, points)
                            VALUES (?, ?, ?, ?, ?)
            """, (
        problem_data.id,
        problem_data.text,
        problem_data.answer,
        problem_data.level,
        problem_data.points
    ))
    con.commit()
    con.close()


def get_problem(id: int):
    con = sqlite3.connect("../../data/NumDuo.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Problems_with_variants WHERE id = ?", (id,))
    res = cursor.fetchall()
    print(res)
    con.close()
    return res


def add_achievement(achieve_data: Achieve):
    con = sqlite3.connect("../../data/NumDuo.db")
    cursor = con.cursor()
    cursor.execute("""
                            INSERT INTO achievement (title, description, picture)
                            VALUES (?, ?, ?)
            """, (
        achieve_data.title,
        achieve_data.description,
        achieve_data.picture
    ))
    con.commit()
    con.close()


def update_username(user_id: int, new_username: str) -> bool:
    try:
        con = sqlite3.connect("../../data/NumDuo.db")
        cursor = con.cursor()

        cursor.execute(
            "UPDATE Users SET username = ?, updateAt = ? WHERE id = ?",
            (new_username, int(time.time()), user_id)
        )
        success = cursor.rowcount > 0
        con.commit()
        con.close()
        return success

    except sqlite3.Error:
        return False


def get_user(user_id: int):
    con = sqlite3.connect("../../data/NumDuo.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
    res = cursor.fetchall()

    con.close()
    return res


def delete_user(user_id: int):
    con = sqlite3.connect("../../data/NumDuo.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
    con.commit()
    rows_deleted = cursor.rowcount
    con.close()
    return rows_deleted


def delete_achievement(achievement_id: int):
    con = sqlite3.connect("../../data/NumDuo.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM achievement WHERE id = ?", (achievement_id,))
    con.commit()
    con.close()
