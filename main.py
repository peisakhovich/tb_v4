from fastapi import FastAPI
import pyodbc
import os
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conn_str_env = os.getenv("DB_CONN_STR")

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": conn_str_env}


@app.get("/db-test")
def db_test():
    try:
        conn = pyodbc.connect(os.getenv("DB_CONN_STR"))
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) From users")

        result = cursor.fetchone()[0]
        conn.close()

        return {"status": "ok", "result": result}

    except Exception as e:
        logger.exception("Database error в БД ошибка")
        return {"status": "error", "detail": str(e)}