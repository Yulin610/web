from sqlalchemy import Column, Float, Integer, String

from app.database.connection import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    authors = Column(String, nullable=False)
    average_rating = Column(Float, nullable=True)
    isbn = Column(String, nullable=True)
    language_code = Column(String, nullable=True)
    num_pages = Column(Integer, nullable=True)
    ratings_count = Column(Integer, nullable=True)
    publication_date = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
