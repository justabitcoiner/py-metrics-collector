from datetime import datetime
import sqlite3

DB_NAME = "metrics.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connect()
    cursor = conn.cursor()
    sql = "CREATE TABLE IF NOT EXISTS func_metrics(func_name, num_calls, num_errors, avg_exec_time, created_time)"
    cursor.execute(sql)


def save_metric(metrics: dict):
    conn = connect()
    cursor = conn.cursor()
    sql = "INSERT INTO func_metrics VALUES(?, ?, ?, ?, ?)"

    sql_params = [
        (key, val.get("num_calls"), val.get("num_errors"), val.get("avg_exec_time"), datetime.now())
        for key, val in metrics.items()
    ]
    cursor.executemany(sql, sql_params)
    conn.commit()
