from psycopg2.extras import execute_values
import yfinance as yf
import datetime as dt
import  pandas as pd

from src.repository.stock_insertion_repositoy import StockInsertionRepository
from src.utils.logging_utils import log_message


class StockInsertionService:
    def __init__(self, request):
        self.request = request

    def insert(self):
        start_date = dt.datetime.today() - dt.timedelta(days=int(self.request.total_days))
        end_date = dt.datetime.today()

        try:
            df = yf.download(
                self.request.stock_id,
                start=start_date,
                end=end_date,
                interval=self.request.stock_interval
            )
            if df.empty:
                log_message("error", "No data fetched for the provided stock ID and interval.")
                return
            log_message(
                "info",
                f"Downloaded data for company: {self.request.stock_name}. "
                f"Rows fetched: {len(df)}"
            )
            company_data = {"company_name": self.request.stock_name, "company_market_id": self.request.stock_id}
            stock_insertion=StockInsertionRepository(self.request)
            company_id =stock_insertion.insert_and_get_company_id(company_data)

            fundamental_analysis_data = self.prepare_fundamental_analysis_data(company_id)
            stock_data = self.prepare_stock_data(df, company_id)
            stock_insertion.insert(company_data,fundamental_analysis_data,stock_data)
            record_count = df.shape[0]
            return record_count
        except Exception as e:
            log_message("error", f"Error processing stock data: {str(e)}")
            return str(e)

    def prepare_fundamental_analysis_data(self, company_id):
      return [
            {
                "stock_period": "2024-Q1",
                "stock_profit": 100000,
                "stock_loss": 50000,
                "stock_cashin": 200000,
                "stock_cashout": 150000,
                "stock_debt": 30000,
                "stock_expenditure": 70000,
                "company_id": company_id,
            }
        ]

    def prepare_stock_data(self, df, company_id):
        prepared_data = []
        for idx, row in df.iterrows():
            stock_data = {
                "company_id": company_id,
                "stock_date": idx.date(),
                "open_price": float(row["Open"].iloc[0]),
                "close_price": float(row["Close"].iloc[0]),
                "high": float(row["High"].iloc[0]) ,
                "low": float(row["Low"].iloc[0]),
                "adj_close": float(row["Adj Close"].iloc[0]),
                "volume": int(row["Volume"].iloc[0]),
            }
            prepared_data.append(stock_data)
        return prepared_data


