import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

app = FastAPI()

app.include_router()


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run("main:app",host="0.0.0.0",port=80,reload=False)


