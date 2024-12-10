import logging

from fastapi import APIRouter
from src.models.models import StockInsertRequest
from src.service.stock_insertion_service import StockInsertService
from src.utils.logging_utils import log_message

router = APIRouter(prefix="/insert",tags=["stock_insertion_api"])


async  def insert_stock(request:StockInsertRequest):
    try:
        log_message("info", f"Request {request}")
        stock_insert_service=StockInsertService(request)
        stock_insert_service.insert()
    except Exception as e:
        log_message("error",f"Inserting is failed stock data in DB. Error {str(e)}")