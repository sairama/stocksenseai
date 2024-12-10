import yfinance as yf
import pandas as pd
import datetime as dt
import numpy as np

import time as t
from src.repository.stock_insertion_repositoy import StockInsertionRepository
from src.utils.logging_utils import log_message
from src.data_dict.cnx_stock_names import get_cnx_company


class StockInsertService:

    def __init__(self,request=None):
        self.request=request

    def insert(self):
        log_message("info","Insertion service is processed")

        cnx_company_dict=get_cnx_company()
        for key, value in cnx_company_dict.items():
            df = yf.download(key, dt.date.today() - dt.timedelta(90), dt.datetime.today(), interval='1d')
            log_message("info", f"The  company name : {value} and the DataFrame : {df}")

        stock_insert_repository=StockInsertionRepository(self.request)
        stock_insert_repository.insert("stock_data")