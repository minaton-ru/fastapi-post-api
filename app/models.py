from sqlalchemy import Column, String, DateTime, Integer, func

from .database import Base


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String, nullable=False)
    question = Column(String, nullable=False)
    category_id = Column(Integer)
    loaded_at = Column(DateTime, default=func.now())
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
