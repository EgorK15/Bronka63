import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, List
from datetime import date, time
from uuid import UUID

class DatabaseConnection:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }

    def __enter__(self):
        self.conn = psycopg2.connect(**self.conn_params)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

class UserOperations:
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection
    def init(self):
        with self.db as conn:
            with conn.cursor() as cur:
                cur.execute(f"""-- Create enum type for user priority
CREATE TYPE user_priority AS ENUM ('prostoi-smertni', 'union', 'prepod', 'dispetcher');

-- Create Users table
CREATE TABLE Users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(50) NOT NULL,
    priority user_priority NOT NULL,
    "group" VARCHAR(50) NOT NULL
);

-- Create Cabinets table
CREATE TABLE Cabinets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    number INTEGER NOT NULL UNIQUE,
    floor INTEGER NOT NULL,
    type TEXT NOT NULL,
    description TEXT
);

-- Create Pairs table
CREATE TABLE Pairs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    day DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    CONSTRAINT check_time_order CHECK (start_time < end_time)
);

-- Create mapping table Pairs_Cabinets
CREATE TABLE Pairs_Cabinets (
    pair_id UUID NOT NULL REFERENCES Pairs(id) ON DELETE CASCADE,
    cabinet_id UUID NOT NULL REFERENCES Cabinets(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES Users(id) ON DELETE CASCADE,
    purpose TEXT,
    PRIMARY KEY (pair_id, cabinet_id)
);

-- Create indexes for better query performance
CREATE INDEX idx_pairs_day ON Pairs(day);
CREATE INDEX idx_cabinets_floor ON Cabinets(floor);
CREATE INDEX idx_pairs_cabinets_user ON Pairs_Cabinets(user_id);
                    """)
                conn.commit()

    def create_or_update_user(self, id: UUID, name: str, username: str, password: str,
                            priority: str, group: int) -> None:
        with self.db as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Users (id, name, username, password, priority, "group")
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (username)
                    DO UPDATE SET
                        name = EXCLUDED.name,
                        password = EXCLUDED.password,
                        priority = EXCLUDED.priority,
                        "group" = EXCLUDED."group"
                    """, (id, name, username, password, priority, group))
                conn.commit()

    def get_user_by_id(self, user_id: UUID) -> Dict:
        with self.db as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM Users WHERE id = %s", (user_id,))
                return cur.fetchone()

    def get_user_by_username(self, username: str) -> Dict:
        with self.db as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM Users WHERE username = %s", (username,))
                return cur.fetchone()

    def delete_user(self, user_id: UUID) -> None:
        with self.db as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Users WHERE id = %s", (user_id,))
                conn.commit()

class CabinetOperations:
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection

    def create_or_update_cabinet(self, id: UUID, number: int, floor: int,
                               type: str, description: str) -> None:
        with self.db as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Cabinets (id, number, floor, type, description)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (number)
                    DO UPDATE SET
                        floor = EXCLUDED.floor,
                        type = EXCLUDED.type,
                        description = EXCLUDED.description
                    """, (id, number, floor, type, description))
                conn.commit()

    def get_cabinet_by_id(self, cabinet_id: UUID) -> Dict:
        with self.db as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM Cabinets WHERE id = %s", (cabinet_id,))
                return cur.fetchone()

    def get_cabinet_by_number(self, number: int) -> Dict:
        with self.db as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM Cabinets WHERE number = %s", (number,))
                return cur.fetchone()

    def delete_cabinet(self, cabinet_id: UUID) -> None:
        with self.db as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Cabinets WHERE id = %s", (cabinet_id,))
                conn.commit()

class PairOperations:
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection

    def create_or_update_pair(self, id: UUID, day: date, start_time: time,
                            end_time: time) -> None:
        with self.db as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO Pairs (id, day, start_time, end_time)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id)
                    DO UPDATE SET
                        day = EXCLUDED.day,
                        start_time = EXCLUDED.start_time,
                        end_time = EXCLUDED.end_time
                    """, (id, day, start_time, end_time))
                conn.commit()

    def get_pair_by_id(self, pair_id: UUID) -> Dict:
        with self.db as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM Pairs WHERE id = %s", (pair_id,))
                return cur.fetchone()

    def get_pairs_by_day(self, day: date) -> List[Dict]:
        with self.db as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM Pairs WHERE day = %s", (day,))
                return cur.fetchall()

    def delete_pair(self, pair_id: UUID) -> None:
        with self.db as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Pairs WHERE id = %s", (pair_id,))
                conn.commit()

class PairsCabinetsOperations:
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection

    def create_or_update_pairs_cabinets(self, pair_id: UUID, cabinet_id: UUID,
                                      user_id: UUID, purpose: str) -> bool:
        with self.db as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    WITH new_mapping AS (
                        SELECT
                            %s as pair_id,
                            %s as cabinet_id,
                            %s as user_id,
                            %s as purpose,
                            (SELECT priority FROM Users WHERE id = %s) as new_priority
                    )
                    INSERT INTO Pairs_Cabinets (pair_id, cabinet_id, user_id, purpose)
                    SELECT
                        pair_id, cabinet_id, user_id, purpose
                    FROM
                        new_mapping
                    ON CONFLICT (pair_id, cabinet_id)
                    DO UPDATE SET
                        user_id = EXCLUDED.user_id,
                        purpose = EXCLUDED.purpose
                    WHERE (
                        SELECT priority FROM Users WHERE id = EXCLUDED.user_id
                    ) > (
                        SELECT priority FROM Users WHERE id = Pairs_Cabinets.user_id
                    )
                    RETURNING id
                    """, (pair_id, cabinet_id, user_id, purpose, user_id))
                result = cur.fetchone()
                conn.commit()
                return result is not None

    def get_pairs_cabinets_info(self, pair_id: UUID) -> List[Dict]:
        with self.db as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT
                        pc.*,
                        p.day,
                        p.start_time,
                        p.end_time,
                        c.number as cabinet_number,
                        c.floor,
                        u.name as user_name,
                        u.priority
                    FROM Pairs_Cabinets pc
                    JOIN Pairs p ON p.id = pc.pair_id
                    JOIN Cabinets c ON c.id = pc.cabinet_id
                    JOIN Users u ON u.id = pc.user_id
                    WHERE pc.pair_id = %s
                    """, (pair_id,))
                return cur.fetchall()

    def delete_pairs_cabinets(self, pair_id: UUID, cabinet_id: UUID) -> None:
        with self.db as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM Pairs_Cabinets
                    WHERE pair_id = %s AND cabinet_id = %s
                    """, (pair_id, cabinet_id))
                conn.commit()

class CabinetScheduleOperations:
    def __init__(self, db_connection: DatabaseConnection):
        self.db = db_connection

    def get_fully_busy_cabinets(self, check_date: date, start_time: time,
                               end_time: time) -> List[Dict]:
        with self.db as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    WITH RECURSIVE time_slots AS (
                        SELECT
                            %s::date as check_date,
                            %s::time as start_time,
                            %s::time as end_time
                    )
                    SELECT DISTINCT
                        c.id as cabinet_id,
                        c.number as cabinet_number,
                        c.floor,
                        c.type,
                        p.day,
                        p.start_time,
                        p.end_time,
                        u.name as reserved_by,
                        u.priority as user_priority,
                        pc.purpose
                    FROM
                        Cabinets c
                        INNER JOIN Pairs_Cabinets pc ON c.id = pc.cabinet_id
                        INNER JOIN Pairs p ON p.id = pc.pair_id
                        INNER JOIN Users u ON u.id = pc.user_id,
                        time_slots ts
                    WHERE
                        p.day = ts.check_date
                        AND p.start_time <= ts.start_time
                        AND p.end_time >= ts.end_time
                    ORDER BY
                        c.floor,
                        c.number,
                        p.start_time
                    """, (check_date, start_time, end_time))
                return cur.fetchall()

    def get_partially_busy_cabinets(self, check_date: date, start_time: time,
                                  end_time: time) -> List[Dict]:
        with self.db as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    WITH RECURSIVE time_slots AS (
                        SELECT
                            %s::date as check_date,
                            %s::time as start_time,
                            %s::time as end_time
                    )
                    SELECT DISTINCT
                        c.id as cabinet_id,
                        c.number as cabinet_number,
                        c.floor,
                        c.type,
                        p.day,
                        p.start_time,
                        p.end_time,
                        u.name as reserved_by,
                        u.priority as user_priority,
                        pc.purpose,
                        CASE
                            WHEN p.start_time <= ts.start_time THEN ts.start_time
                            ELSE p.start_time
                        END as overlap_start,
                        CASE
                            WHEN p.end_time >= ts.end_time THEN ts.end_time
                            ELSE p.end_time
                        END as overlap_end
                    FROM
                        Cabinets c
                        INNER JOIN Pairs_Cabinets pc ON c.id = pc.cabinet_id
                        INNER JOIN Pairs p ON p.id = pc.pair_id
                        INNER JOIN Users u ON u.id = pc.user_id,
                        time_slots ts
                    WHERE
                        p.day = ts.check_date
                        AND (
                            (p.start_time < ts.end_time AND p.start_time >= ts.start_time)
                            OR (p.end_time > ts.start_time AND p.end_time <= ts.end_time)
                        )
                        AND NOT (p.start_time <= ts.start_time AND p.end_time >= ts.end_time)
                    ORDER BY
                        c.floor,
                        c.number,
                        p.start_time
                    """, (check_date, start_time, end_time))
                return cur.fetchall()

    def get_free_cabinets(self, check_date: date, start_time: time,
                         end_time: time) -> List[Dict]:
        with self.db as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    WITH RECURSIVE time_slots AS (
                        SELECT
                            %s::date as check_date,
                            %s::time as start_time,
                            %s::time as end_time
                    )
                    SELECT
                        c.id as cabinet_id,
                        c.number as cabinet_number,
                        c.floor,
                        c.type,
                        c.description
                    FROM
                        Cabinets c
                    WHERE
                        NOT EXISTS (
                            SELECT 1
                            FROM Pairs_Cabinets pc
                            JOIN Pairs p ON p.id = pc.pair_id,
                            time_slots ts
                            WHERE
                                pc.cabinet_id = c.id
                                AND p.day = ts.check_date
                                AND (
                                    (p.start_time <= ts.start_time AND p.end_time > ts.start_time)
                                    OR (p.start_time < ts.end_time AND p.end_time >= ts.end_time)
                                    OR (p.start_time >= ts.start_time AND p.end_time <= ts.end_time)
                                )
                        )
                    ORDER BY
                        c.floor,
                        c.number
                    """, (check_date, start_time, end_time))
                return cur.fetchall()

    def get_cabinet_schedule(self, cabinet_id: UUID, check_date: date) -> List[Dict]:
        with self.db as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    WITH RECURSIVE time_ranges AS (
    SELECT
        %s::uuid as cabinet_id,
        %s::date as check_date
)
SELECT
    c.number as cabinet_number,
    c.floor,
    c.type,
    p.day,
    p.start_time,
    p.end_time,
    u.name as reserved_by,
    u.username,
    u.priority as user_priority,
    pc.purpose,
    -- Добавляем расчет длительности брони
    (EXTRACT(EPOCH FROM p.end_time - p.start_time)/3600)::numeric(10,2) as duration_hours,
    -- Добавляем информацию о следующем свободном промежутке
    LEAD(p.start_time) OVER (ORDER BY p.start_time) as next_booking_starts,
    CASE
        WHEN LEAD(p.start_time) OVER (ORDER BY p.start_time) IS NOT NULL
        THEN (EXTRACT(EPOCH FROM LEAD(p.start_time) OVER (ORDER BY p.start_time) - p.end_time)/3600)::numeric(10,2)
        ELSE NULL
    END as free_time_until_next_booking
FROM
    Cabinets c
    INNER JOIN Pairs_Cabinets pc ON c.id = pc.cabinet_id
    INNER JOIN Pairs p ON p.id = pc.pair_id
    INNER JOIN Users u ON u.id = pc.user_id,
    time_ranges tr
WHERE
    c.id = tr.cabinet_id
    AND p.day = tr.check_date
ORDER BY
    p.start_time;
""", (cabinet_id, check_date))
                return cur.fetchall()

con = DatabaseConnection("fast_api","postgres","postgres","localhost", "5433")

user_operations =UserOperations(con)
pairs = PairOperations(con)

print(pairs.create_or_update_pair("a4b34841-0f60-4d14-a0af-ee7190f39d46","2025-01-01","10:10:10","11:11:11"))
print(pairs.get_pairs_by_day("2025-01-01"))
print(pairs.get_pair_by_id("a4b34841-0f60-4d14-a0af-ee7190f39d46"))
print(pairs.delete_pair("a4b34841-0f60-4d14-a0af-ee7190f39d46"))
