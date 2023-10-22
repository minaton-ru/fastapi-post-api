import aiohttp
from typing import List


async def get_new_quiz_from_jservice(questions_count: int) -> List[dict]:
    """
    Загрузка вопрсов с сервиса jService.
    На вход принимает int число вопросов, которые нужно загрузить.
    Возвращает список словарей с данными вопросов.
    """
    URL = f"https://jservice.io/api/random?count={questions_count}"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            new_questions = await response.json()
    return new_questions
