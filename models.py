from sqlalchemy import Column, Integer, String
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)
    email = Column(String)

    country = Column(String)
    timezone = Column(String)

    interests = Column(String)
    languages = Column(String)

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)

    student_1_id = Column(Integer)
    student_2_id = Column(Integer)

    status = Column(String)  # pending, accepted