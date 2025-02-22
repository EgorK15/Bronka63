-- Users CRUD Operations
-- Create/Update User
INSERT INTO Users (id, name, username, password, priority, "group")
VALUES ('da8f29e9-fa83-4e8d-98e2-0e2649841b98', 1, 1, 1, 'dispetcher', 1)
ON CONFLICT (username)
DO UPDATE SET
    name = EXCLUDED.name,
    password = EXCLUDED.password,
    priority = EXCLUDED.priority,
    "group" = EXCLUDED."group";

-- Read User
SELECT * FROM Users WHERE id = 'da8f29e9-fa83-4e8d-98e2-0e2649841b98';
SELECT * FROM Users WHERE username = '1';

-- Delete User
DELETE FROM Users WHERE id = 1;

-- Cabinets CRUD Operations
-- Create/Update Cabinet
INSERT INTO Cabinets (id, number, floor, type, description)
VALUES ('da8f29e9-fa83-4e8d-98e2-0e2649841b98',111, 1, 'a', 'a')
ON CONFLICT (number)
DO UPDATE SET
    floor = EXCLUDED.floor,
    type = EXCLUDED.type,
    description = EXCLUDED.description;

-- Read Cabinet
SELECT * FROM Cabinets WHERE id = $1;
SELECT * FROM Cabinets WHERE number = $1;

-- Delete Cabinet
DELETE FROM Cabinets WHERE id = $1;

-- Pairs CRUD Operations
-- Create/Update Pair
INSERT INTO Pairs (id, day, start_time, end_time)
VALUES ($1, $2, $3, $4)
ON CONFLICT (id)
DO UPDATE SET
    day = EXCLUDED.day,
    start_time = EXCLUDED.start_time,
    end_time = EXCLUDED.end_time;

-- Read Pair
SELECT * FROM Pairs WHERE id = $1;
SELECT * FROM Pairs WHERE day = $1;

-- Delete Pair
DELETE FROM Pairs WHERE id = $1;

-- Pairs_Cabinets CRUD Operations with Priority Check
-- Create/Update Pairs_Cabinets with Priority Logic
WITH new_mapping AS (
    SELECT
        $1 as pair_id,
        $2 as cabinet_id,
        $3 as user_id,
        $4 as purpose,
        (SELECT priority FROM Users WHERE id = $3) as new_priority
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
);

-- Read Pairs_Cabinets
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
WHERE pc.pair_id = $1;

-- Delete Pairs_Cabinets
DELETE FROM Pairs_Cabinets
WHERE pair_id = $1 AND cabinet_id = $2;


-- Function to get cabinets that are busy for the entire period
WITH RECURSIVE time_slots AS (
    SELECT
        $1::date as check_date,
        $2::time as start_time,
        $3::time as end_time
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
    p.start_time;

-- Function to get cabinets that are partially busy during the period
WITH RECURSIVE time_slots AS (
    SELECT
        $1::date as check_date,
        $2::time as start_time,
        $3::time as end_time
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
    p.start_time;

-- Example usage:
-- For fully busy cabinets:
-- SELECT * FROM get_fully_busy_cabinets('2024-02-20', '09:00', '10:30');
-- For partially busy cabinets:
-- SELECT * FROM get_partially_busy_cabinets('2024-02-20', '09:00', '10:30');

-- Function to get completely free cabinets for the period
WITH RECURSIVE time_slots AS (
    SELECT
        $1::date as check_date,
        $2::time as start_time,
        $3::time as end_time
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
    c.number;

-- Function to get all busy periods for a specific cabinet on a given date
WITH RECURSIVE time_ranges AS (
    SELECT
        $1::uuid as cabinet_id,
        $2::date as check_date
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

-- Example usage:
-- For free cabinets:
-- SELECT * FROM get_free_cabinets('2024-02-20', '09:00', '10:30');
-- For cabinet schedule:
-- SELECT * FROM get_cabinet_schedule('cabinet-uuid', '2024-02-20');

