from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from uuid import UUID

app = FastAPI()

# Подключение к базе данных
def get_db_connection():
    conn = psycopg2.connect(
        dbname="fast_api",
        user="postgres",
        password="postgres",
        host="localhost",
        port = "5433",
        cursor_factory=RealDictCursor
    )
    return conn

# Модели Pydantic для валидации данных
class User(BaseModel):
    name: str
    username: str
    password: str
    priority: str
    group: str

class Cabinet(BaseModel):
    number: int
    floor: int
    type: str
    description: str

class Pair(BaseModel):
    day: str
    start_time: str
    end_time: str

class PairCabinet(BaseModel):
    pair_id: UUID
    cabinet_id: UUID
    user_id: UUID
    purpose: str

# CRUD операции для Users
@app.post("/users/", response_model=User)
def create_user(user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Users (name, username, password, priority, "group")
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
        """,
        (user.name, user.username, user.password, user.priority, user.group)
    )
    new_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_user

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: UUID):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users WHERE id = %s;", (str(user_id),))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE Users
        SET name = %s, username = %s, password = %s, priority = %s, "group" = %s
        WHERE id = %s
        RETURNING *;
        """,
        (user.name, user.username, user.password, user.priority, user.group, str(user_id))
    )
    updated_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}")
def delete_user(user_id: UUID):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Users WHERE id = %s RETURNING *;", (str(user_id),))
    deleted_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# CRUD операции для Cabinets
@app.post("/cabinets/", response_model=Cabinet)
def create_cabinet(cabinet: Cabinet):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Cabinets (number, floor, type, description)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
        """,
        (cabinet.number, cabinet.floor, cabinet.type, cabinet.description)
    )
    new_cabinet = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_cabinet

@app.get("/cabinets/{cabinet_id}", response_model=Cabinet)
def read_cabinet(cabinet_id: UUID):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Cabinets WHERE id = %s;", (str(cabinet_id),))
    cabinet = cur.fetchone()
    cur.close()
    conn.close()
    if cabinet is None:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    return cabinet

@app.put("/cabinets/{cabinet_id}", response_model=Cabinet)
def update_cabinet(cabinet_id: UUID, cabinet: Cabinet):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE Cabinets
        SET number = %s, floor = %s, type = %s, description = %s
        WHERE id = %s
        RETURNING *;
        """,
        (cabinet.number, cabinet.floor, cabinet.type, cabinet.description, str(cabinet_id))
    )
    updated_cabinet = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated_cabinet is None:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    return updated_cabinet

@app.delete("/cabinets/{cabinet_id}")
def delete_cabinet(cabinet_id: UUID):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Cabinets WHERE id = %s RETURNING *;", (str(cabinet_id),))
    deleted_cabinet = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted_cabinet is None:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    return {"message": "Cabinet deleted successfully"}

# CRUD операции для Pairs
@app.post("/pairs/")
def create_pair(pair: Pair):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Pairs (day, start_time, end_time)
        VALUES (%s, %s, %s)
        RETURNING *;
        """,
        (pair.day, pair.start_time, pair.end_time)
    )
    new_pair = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_pair

@app.get("/pairs/{pair_id}")
def read_pair(pair_id: UUID):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Pairs WHERE id = %s;", (str(pair_id),))
    pair = cur.fetchone()
    cur.close()
    conn.close()
    if pair is None:
        raise HTTPException(status_code=404, detail="Pair not found")
    return pair

@app.put("/pairs/{pair_id}")
def update_pair(pair_id: UUID, pair: Pair):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE Pairs
        SET day = %s, start_time = %s, end_time = %s
        WHERE id = %s
        RETURNING *;
        """,
        (pair.day, pair.start_time, pair.end_time, str(pair_id))
    )
    updated_pair = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated_pair is None:
        raise HTTPException(status_code=404, detail="Pair not found")
    return updated_pair

@app.delete("/pairs/{pair_id}")
def delete_pair(pair_id: UUID):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Pairs WHERE id = %s RETURNING *;", (str(pair_id),))
    deleted_pair = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted_pair is None:
        raise HTTPException(status_code=404, detail="Pair not found")
    return {"message": "Pair deleted successfully"}

# CRUD операции для Pairs_Cabinets
@app.post("/pairs_cabinets/", response_model=PairCabinet)
def create_pair_cabinet(pair_cabinet: PairCabinet):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Pairs_Cabinets (pair_id, cabinet_id, user_id, purpose)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
        """,
        (str(pair_cabinet.pair_id), str(pair_cabinet.cabinet_id), str(pair_cabinet.user_id), pair_cabinet.purpose)
    )
    new_pair_cabinet = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return new_pair_cabinet

@app.get("/pairs_cabinets/{pair_id}/{cabinet_id}", response_model=PairCabinet)
def read_pair_cabinet(pair_id: UUID, cabinet_id: UUID):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Pairs_Cabinets WHERE pair_id = %s AND cabinet_id = %s;", (str(pair_id), str(cabinet_id)))
    pair_cabinet = cur.fetchone()
    cur.close()
    conn.close()
    if pair_cabinet is None:
        raise HTTPException(status_code=404, detail="PairCabinet not found")
    return pair_cabinet

@app.delete("/pairs_cabinets/{pair_id}/{cabinet_id}")
def delete_pair_cabinet(pair_id: UUID, cabinet_id: UUID):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Pairs_Cabinets WHERE pair_id = %s AND cabinet_id = %s RETURNING *;", (str(pair_id), str(cabinet_id)))
    deleted_pair_cabinet = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if deleted_pair_cabinet is None:
        raise HTTPException(status_code=404, detail="PairCabinet not found")
    return {"message": "PairCabinet deleted successfully"}

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)