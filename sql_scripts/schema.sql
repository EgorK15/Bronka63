-- Create enum type for user priority
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