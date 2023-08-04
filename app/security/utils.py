from passlib.context import CryptContext

from app.schemas import UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(user_db, username: str, password: str):
    user = get_user(user_db, username)
    if not user:
        return False
    if not verify(password, user.hashed_password):
        return False
    return user
