from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class CarCredential(Base):
    __tablename__ = 'cars_credentials'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    price_usd = Column(Float)
    odometer = Column(Integer)
    username = Column(String)
    phone_number = Column(String)
    image_url = Column(String)
    images_count = Column(Integer)
    car_number = Column(String)
    car_vin = Column(String)
    datetime_found = Column(DateTime, default=func.now())


engine = create_engine('postgresql://postgres:stas123@db:5432/postgres')
Session = sessionmaker(bind=engine)
session = Session()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
