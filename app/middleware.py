import os
import datetime

from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from pymongo import MongoClient

DBHOST = os.environ.get("MONGO_HOST", "localhost")
DBPORT = os.environ.get("MONGO_PORT", "27017")
DBNAME = os.environ.get("MONGO_DBNAME", "planner")
USER = os.environ.get("MONGO_USER", "mongo")
PASSWORD = os.environ.get("MONGO_PASSWORD", "mongo")

def get_mongoDB_connect():
    """
        mongoDB에 접근하기 위한 connect 반환
    """
    MONGO_URL = f"mongodb://{USER}:{PASSWORD}@{DBHOST}:{DBPORT}"
    return MongoClient(MONGO_URL)[DBNAME]

class LogMiddleWare(BaseHTTPMiddleware):
    """
        mongoDB 서버에 로그를 남기기 위한 middleware
    """
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request:Request, call_next):
        """
            1. get connect
            2. method, url, created_at 저장
        """
        conn = get_mongoDB_connect()
        logs = conn["logs"]

        log_data = {
            "method": request.method,
            "url": str(request.url),
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        logs.insert_one(log_data)
        
        res = await call_next(request)
        return res