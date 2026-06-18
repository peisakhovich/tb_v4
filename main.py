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
        cursor.execute("select  N'Количество записей в таблице Users' + str(count(*)) + N' Сейчас:' + cast(SYSDATETIME() as nvarchar(30))  from users")

        result = cursor.fetchone()[0]
        
        cur = conn.cursor()

        cur.execute("""
                SELECT
                @@SERVERNAME AS ServerName,
                DB_NAME() AS DatabaseName,
                GETDATE() AS CurrentTime
                """)

        row = cur.fetchone()



        conn.close()

        return {"status": "ok", "result": result, "server": row.ServerName,
        "database": row.DatabaseName,
        "time": str(row.CurrentTime)}

    except Exception as e:
        logger.exception("Database error в БД ошибка")
        return {"status": "error", "detail": str(e)}