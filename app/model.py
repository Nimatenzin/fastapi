from sqlalchemy import Column, Integer, String, JSON, TEXT
from sqlalchemy.dialects.postgresql import JSON, TEXT
from config import Base



class Book(Base):
    __tablename__ = 'book'

    id=Column(Integer, primary_key=True)
    title=Column(String)
    description= Column(String)


 

class FileData(Base):
    __tablename__ = "file_data"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content = Column(JSON)  # Adjust the length based on your requirements


class CsvData(Base):
    __tablename__ = 'csv_data'

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    content = Column(TEXT) 



