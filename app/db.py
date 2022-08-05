import os

import psycopg2

from .models import UserInDB

DBHOST = os.environ.get("POSTGRES_HOST", "localhost")
DBPORT = os.environ.get("POSTGRES_PORT", "5432")
DBNAME = os.environ.get("POSTGRES_DBNAME", "admin")
USER = os.environ.get("POSTGRES_USER", "postgres")
PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")

## default
def get_connect():
    conn = psycopg2.connect(host=DBHOST, port=DBPORT, 
                            dbname=DBNAME, 
                            user=USER, password=PASSWORD)
    conn.autocommit = True
    return conn

## Users
def get_user(username):
    sql = """
        SELECT username, hashed_password FROM Users 
        WHERE username=%s"""

    conn = get_connect()
    cur = conn.cursor()
    cur.execute(sql, (username,))

    user = cur.fetchone()
    # convert user
    if user:
        (username_, hashed_password_) = user
        user = UserInDB(username=username_, hashed_password=hashed_password_)

    cur.close()
    conn.close()
    return user

def register_user(username, hased_password, email, full_name):
    sql = """
        INSERT INTO Users 
        (username, hashed_password, email, full_name) 
        VALUES (%s, %s, %s, %s)
    """
    
    conn = get_connect()
    cur = conn.cursor()
    cur.execute(sql, (username, hased_password, email, full_name,))
    cur.close()
    conn.close()
## /Users

## Planner
def get_plans(username, title=None):
    sql = """
        SELECT id, date, title, score, memo FROM planner
        WHERE username=%s"""
    if title:
        sql += f" AND title='{title}'"

    conn = get_connect()
    cur = conn.cursor()
    cur.execute(sql, (username,))
    plans = []
    for (id_, date, title_, score, memo) in cur.fetchall():
        plans.append(dict(id=id_, date=date, title=title_, score=score, memo=memo))

    cur.close()
    conn.close()
    return plans
    
def register_plan(username, date, title, score, memo):
    sql = """
        INSERT INTO Planner 
        (username, date, title, score, memo) 
        VALUES (%s, %s, %s, %s, %s)
    """
    
    conn = get_connect()
    cur = conn.cursor()
    cur.execute(sql, (username, date, title, score, memo,))
    cur.close()
    conn.close()

def update_plan(plan_id, title, score, memo):
    sql = """
        UPDATE Planner
        SET title=%s, score=%s, memo=%s
        WHERE id=%s
    """
    
    conn = get_connect()
    cur = conn.cursor()
    cur.execute(sql, (title, score, memo, plan_id))
    cur.close()
    conn.close()

def delete_plan(plan_id):
    sql = """
        DELETE FROM Planner
        WHERE id=%s
    """

    conn = get_connect()
    cur = conn.cursor()
    cur.execute(sql, (plan_id, ))
    cur.close()
    conn.close()

## Summary
def get_score_per_key(username, pivot=None):
    """
        월, 일, 주 별 평균 점수 반환
    """
    if not pivot or pivot not in ["month", "day", "week"]: # 월, 일, 주
        return []

    table = {
        "month":"MM", 
        "day":"DD", 
        "week":"D"
    }

    sql = """
        SELECT TO_CHAR(date, %s), ROUND(SUM(score)/COUNT(score), 2)
        FROM Planner
        WHERE username = %s
        GROUP BY 1
        ORDER BY 1
    """
    results = []
    with get_connect() as conn, conn.cursor() as cur:
        cur.execute(sql, (table[pivot], username, ))
        for (key, aver_score) in cur.fetchall():
            results.append({"key": key, "score":aver_score})

    return results

def get_score_per_plan(username, order=""):
    """
        계획 별 점수
    """
    order = order.upper()
    if not order or order not in ["ASC", "DESC"]: # 오름 차순
        return []

    sql = f"""
        SELECT title, ROUND(SUM(score)/COUNT(score), 2)
        FROM Planner
        WHERE username = %s
        GROUP BY 1
        ORDER BY 2 {order}
        LIMIT 10
    """
    results = []
    with get_connect() as conn, conn.cursor() as cur:
        cur.execute(sql, (username, ))
        for (key, aver_score) in cur.fetchall():
            results.append({"key": key, "score":aver_score})

    return results

def get_freq_plan(username):
    """
        자주 세운 계획
    """
    sql = f"""
        SELECT title, COUNT(*)
        FROM Planner
        WHERE username = %s
        GROUP BY 1
        ORDER BY 2 DESC
        LIMIT 10
    """
    results = []
    with get_connect() as conn, conn.cursor() as cur:
        cur.execute(sql, (username, ))
        for (key, cnt) in cur.fetchall():
            results.append({"key": key, "count": cnt})

    return results
## /Summary