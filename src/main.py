import os
from fastapi import FastAPI, APIRouter
import psycopg
import redis

app = FastAPI()

health_router = APIRouter()
deps_router = APIRouter()

@health_router.get("/health")
def health():
    return "ok"

@deps_router.get("/deps")
def deps():

    try:
        with psycopg.connect(
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            dbname=os.environ["DB_NAME"],
            connect_timeout=3,
        ) as conn:
            db_status = conn.execute("SELECT 1").fetchone()
            db_status = "ok"

    except Exception as e:
        db_status = f"DB Error: {e}"

    
    try:
        r = redis.Redis(
            host=os.environ["REDIS_HOST"], 
            password=os.environ["REDIS_PASSWORD"], 
            port=os.environ["REDIS_PORT"],
            socket_connect_timeout=2,
            socket_timeout=2
        )
        r.ping()
        redis_status = "ok"
    except Exception as e:
        redis_status = f"Redis error: {e}"

    return {
        "DB": db_status,
        "Redis": redis_status
    }

app.include_router(health_router)
app.include_router(deps_router)