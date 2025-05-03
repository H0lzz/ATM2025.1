from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", summary="Hello World")
def root():
    return {"message": "Hello World from ATM Backend!"}

@app.get("/docs", include_in_schema=False)
def redirect_to_swagger():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")