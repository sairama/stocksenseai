from pydantic import BaseModel


class StockInsertRequest(BaseModel):
    stock_name:str
    stock_id:str
    stock_start_date:str
    stock_end_date:str
    stock_period:str = None
