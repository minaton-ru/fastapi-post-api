from fastapi import FastAPI

from routers import question

app = FastAPI()

app.include_router(question.router, tags=['Question'], prefix='/api/question')


@app.get('/')
def root():
    return {'message': 'Hello World'}
