from sqlalchemy import create_engine, Column, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class MachineReading(Base):
    __tablename__ = "machine_readings"
    id = Column(String, primary_key=True)
    machine_id = Column(String, index=True)
    temperature = Column(Float)
    pressure = Column(Float)
    vibration = Column(Float)
    power_consumption = Column(Float)
    timestamp = Column(DateTime)

SQLALCHEMY_DATABASE_URL = "sqlite:///./digital_twin.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)