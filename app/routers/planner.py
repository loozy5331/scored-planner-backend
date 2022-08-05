from fastapi import APIRouter, Header, Depends, Form

from .. import db
from ..exceptions import CREDENTIALS_EXCEPTION

async def check_token(Authorization: str = Header(...)): 
    if not Authorization:
        raise CREDENTIALS_EXCEPTION
    return True

router = APIRouter(
    prefix="/plan",
    tags=["plan"],
    dependencies=[Depends(check_token)],
    responses={404: {"description": "Not fount"}}
)

@router.post("/{username}")
def add_plan(username:str, date:str=Form(...), title:str=Form(...), score:int=Form(...), memo:str=Form(...)):
    if username == "guest":
        return dict(status=200)

    db.register_plan(username, date, title, score, memo)
    return dict(status=200)

@router.put("/{username}/{plan_id}")
def update_plan(username:str, plan_id:str, title:str=Form(...), score:int=Form(...), memo:str=Form(...)):
    if username == "guest":
        return dict(status=200)

    db.update_plan(plan_id, title, score, memo)
    return dict(status=200)

@router.get("/{username}")
def get_plans(username:str, title: str = None):
    return {"plans": db.get_plans(username, title)}

@router.delete("/{username}/{plan_id}")
def delete_plan(username:str, plan_id:int):
    if username == "guest":
        return dict(status=200)
        
    db.delete_plan(plan_id)
    return dict(status=200)