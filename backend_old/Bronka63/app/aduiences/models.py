from sqlalchemy import ForeignKey, text, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base, str_uniq, int_pk, str_null_true
from datetime import date, time


#Описание таблицы
class Users(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    username: Mapped[str_uniq]
    password: Mapped[str]
    priority: Mapped[int]
    group: Mapped[str] # этачевапшетакое

    def __repr__(self):
        return str(self)    

class Cabinets(Base):
    id: Mapped[int_pk]
    number: Mapped[int_pk] #Тут ловушка
    floor: Mapped[int]
    type: Mapped[text]
    description: Mapped[str]

    def __repr__(self):
        return str(self)   

class Pair(Base):
    id: Mapped[int_pk]
    day: Mapped[date]
    start_time: Mapped[time]
    end_time: Mapped[time]
    check_time_order: Mapped[bool] #Тут тоже ловушка

    def __repr__(self):
        return str(self)
    
class Pair_Cabinets(Base):
    pair_id: Pair[id]
    cabinet_id: Cabinets[id]
    user_id: Users[id]
    purporse: Mapped[text]
    primary_key: Mapped[int_pk]

    def __repr__(self):
        return str(self)
    

    

