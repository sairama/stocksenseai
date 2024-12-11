import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from src.api import stock_insertion_api

app = FastAPI()

app.include_router(stock_insertion_api.router)


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("main:app",host="0.0.0.0",port=80,reload=False)


