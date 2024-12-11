from fastapi import APIRouter
from src.models.models import StockInsertRequest
from src.service.stock_insertion_service import StockInsertionService
from src.utils.logging_utils import log_message

router = APIRouter(prefix="/stock",tags=["stock_insertion_api"])


@router.post("/insert")
async def insert_stock(request:StockInsertRequest):
    try:
        log_message("info", f"Request {request}")
        stock_insert_service=StockInsertionService(request)
        stock_count = stock_insert_service.insert()
        return f"Successfully insert data in DB the Stock count : {stock_count}"
    except Exception as e:
        log_message("error",f"Inserting is failed stock data in DB. Error {str(e)}")