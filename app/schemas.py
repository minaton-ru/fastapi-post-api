from datetime import datetime
from pydantic import BaseModel


class QuestionsNum(BaseModel):
    questions_num: int


class QuestionBaseSchema(BaseModel):
    answer: str
    question: str

    class Config:
        from_attributes = True


class CreateQuestionSchema(QuestionBaseSchema):
    id: int
    category_id: int
    created_at: datetime
    updated_at: datetime
