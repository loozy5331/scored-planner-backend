from fastapi import APIRouter, Header, Depends

from .. import db
from ..exceptions import CREDENTIALS_EXCEPTION

# async def check_token(Authorization: str = Header(...)): 
#     if not Authorization:
#         raise CREDENTIALS_EXCEPTION
#     return True

router = APIRouter(
    prefix="/graph",
    tags=["graph"],
    # dependencies=[Depends(check_token)],
    responses={404: {"description": "Not fount"}}
)

@router.get("/{pivot}/{username}")
def get_score_per_pivot(pivot:str, username:str):
    """
        pivot 기간 별 평균 점수
        (pivot == month)
         - key: int = 1~12
        (pivot == day)
         - key: int = 1~31
        (pivot == week)
         - key: 1~7 (Sunday ~ Saturday)
    """
    results = dict() # x월: score
    objects = db.get_score_per_key(username, pivot)
    for obj in objects:
        key = int(obj['key']) # "01" -> 1
        results[key] = obj["score"]

    return results

@router.get("/plan/{pivot}/{username}")
def get_dataset_per_title(username:str, pivot:str): 
    """
        (pivot == "freq")
            - 자주 세운 계획
            - [{ key : title, count : count}]
        (pivot in ["ASC", "DESC"])
            - 계획 별 평균 점수
            - [{ key : title, score : score}]
    """
    if pivot == "freq":
        return db.get_freq_plan(username)
    else:
        return db.get_score_per_plan(username, pivot) # list