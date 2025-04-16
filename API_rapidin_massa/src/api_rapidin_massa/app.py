from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def lendo_raiz():
    return {'message': 'Raios Funde'}
