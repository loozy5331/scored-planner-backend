from datetime import timedelta

from fastapi import Depends, APIRouter, Form
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import pwd_context, create_access_token, get_current_username
from ..exceptions import INCORRECT_ID_OR_PASS_EXCEPTION, DUPLICATED_USER_EXCEPTION

from ..db import get_user, register_user

ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    """
        1. DB에서 user 불러오기
        2. 비밀번호 확인 검사
    """
    # 1.
    user = get_user(username)
    if not user:
        return False
    # 2.
    if not verify_password(password, user.hashed_password):
        return False

    return user

@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
        로그인

        1. DB에서 user 확인
        2. 토큰 발급
    """
    # 1.
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise INCORRECT_ID_OR_PASS_EXCEPTION
    # 2. 
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signUp")
async def signUp(username:str=Form(...), password:str=Form(...), email:str = Form(...), full_name:str = "default"):
    """
        회원가입
        1. 이미 가입했는지 확인
        2. 없다면 DB 추가
        3. token 발급
    """
    # 1.
    user = get_user(username)
    if user:
        raise DUPLICATED_USER_EXCEPTION

    # 2.
    register_user(username, get_password_hash(password), email, full_name)

    # 3.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/getUserName")
async def get_username(username:str=Depends(get_current_username)):
    """
        token을 통해 username 획득
    """
    return {"username": username}