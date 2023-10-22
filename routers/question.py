import aiohttp

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import exists
from fastapi import HTTPException, Depends, status, APIRouter

from app.database import get_db
from app import schemas, models
from app.utils import get_new_quiz_from_jservice
from app.crud import create_question


router = APIRouter()


async def check_unique_question(question_data: schemas.CreateQuestionSchema,
                                db: Session) -> models.Question | None:
    """
    Проверяет наличие в БД вопроса по его id. Если вопрос с таким id уже
    существует в БД, то запрашивает с сервиса jService еще один вопрос и
    рекурсивно проверяет его id. Если вопроса с таким id не существует в БД,
    то передает его данные в функцию для записи вопроса в БД.

    На вход получает словарь с данными вопроса с jService.
    """
    id = question_data["id"]

    if db.query(exists().where(models.Question.id == id)).scalar():

        # Проверяем количество вопросов в нашей базе. Их не может быть больше,
        # чем есть у сервиса jService
        count = db.query(models.Question).count()
        if count == 221510:
            raise HTTPException(status_code=406,
                                detail="Exceeded the number of questions")

        try:
            data = await get_new_quiz_from_jservice(1)
        except aiohttp.ClientConnectorError:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE)
        await check_unique_question(data[0], db)

    else:
        return create_question(question_data, db)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def load_and_create_questions(params: schemas.QuestionsNum,
                                    db: Session = Depends(get_db)):
    """
    Ендпойнт принимает POST запрос в виде:
    {"questions_num": N}
    где N - количество вопросов, которые нужно загрузить.
    Загружает указанное количество вопросов с сервиса jService и записывает
    уникальные вопросы в БД.
    Возвращает предыдущий сохраненный в БД вопрос.
    """
    try:
        data = await get_new_quiz_from_jservice(params.questions_num)
    except aiohttp.ClientConnectorError:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE)

    for questions_data in data:
        try:
            await check_unique_question(questions_data, db)
        except IntegrityError as exception:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"statement": exception.statement,
                        "params": exception.params},
            )

    # Из вопросов, отсортированных по дате сохранения в БД,
    # берем один начиная со второго.
    last_previous = (
        db.query(models.Question)
        .order_by(models.Question.loaded_at.desc())
        .offset(1).limit(1).all()
    )

    return last_previous
