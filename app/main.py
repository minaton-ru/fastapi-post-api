from fastapi import FastAPI

from routers import question

app = FastAPI()

# Ендопойнты для основного API находятся в файле routers/question.py
app.include_router(question.router, tags=['Question'], prefix='/api/question')


@app.get('/')
def root():
    return {'message': 'Please navigate to /docs'}
