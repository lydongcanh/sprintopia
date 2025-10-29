from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def read_root():
    return "Hello, welcome to Sprintopia Service Host! Docs are at /docs, /redoc."


@app.get("/healthz")
async def health_check():
    return {"status": "ok"}