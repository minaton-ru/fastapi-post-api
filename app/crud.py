from sqlalchemy.orm import Session

from app import schemas, models


def create_question(question_data: schemas.CreateQuestionSchema,
                    db: Session) -> models.Question:
    """
    Создание и запись в БД нового вопроса.
    На вход получает словарь с данными.
    Возвращает сохраненный в БД вопрос.
    """
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
