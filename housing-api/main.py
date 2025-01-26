from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:514nA78.@localhost:5432/housing_db"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

class House(Base):
    __tablename__ = 'houses'
    id = Column(Integer, primary_key=True, index=True)
    longitude = Column(Float)
    latitude = Column(Float)
    housing_median_age = Column(Integer)
    total_rooms = Column(Integer)
    total_bedrooms = Column(Integer)
    population = Column(Integer)
    households = Column(Integer)
    median_income = Column(Float)
    median_house_value = Column(Float)
    ocean_proximity = Column(String)

Base.metadata.create_all(bind=engine)

@app.get("/houses")
def get_houses():
    db = SessionLocal()
    houses = db.query(House).all()
    db.close()
    return houses

@app.post("/houses")
def add_house(house: House):
    db = SessionLocal()
    db.add(house)
    db.commit()
    db.close()
    return {"message": "House added successfully"}
