import aiohttp
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends, status, APIRouter

from app.database import get_db
from app import schemas, models


router = APIRouter()


async def get_new_questions_from_jservice(questions_count: int) -> dict | None:
    URL = f"https://jservice.io/api/random?count={questions_count}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            new_questions = await response.json()
    return new_questions


def create_question(question_data: schemas.CreateQuestionSchema,
                    db: Session):
    new_question = models.Question(
        id=question_data["id"],
        answer=question_data["answer"],
        question=question_data["question"],
        category_id=question_data["category_id"],
        created_at=question_data["created_at"],
        updated_at=question_data["updated_at"]
        )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


@router.post('/', status_code=status.HTTP_201_CREATED)
async def load_and_create_questions(params: schemas.QuestionsNum,
                                    db: Session = Depends(get_db)):
    data = await get_new_questions_from_jservice(params.questions_num)
    for questions_data in data:
        try:
            create_question(questions_data, db)
        except IntegrityError as exception:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"statement": exception.statement,
                        "params": exception.params},
            )
    last_previous = db.query(models.Question).order_by(models.Question.loaded_at.desc()).offset(1).limit(1).all()
    return last_previous
