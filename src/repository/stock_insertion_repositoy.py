from src.utils.database_utils import get_db_connection
from src.utils.logging_utils import log_message
from psycopg2.extras import execute_values

class StockInsertionRepository:

    def __init__(self,request=None):
        self.request=request
        self.db_connection=get_db_connection()

    def insert(self,company_data,fundamental_analysis_data,stock_data):
        log_message("info","Insertion repository process")
        if self.db_connection:
            try:
                cursor=self.db_connection.cursor()
                self.insert_sql(cursor,company_data,fundamental_analysis_data,stock_data)
                self.db_connection.commit()
            except Exception as e:
                log_message("error", f"Insertion Failed error : {str(e)}")
            finally:
                self.db_connection.close()
        else:
            raise ValueError("Failed to connect to database while calling the insert")

    def insert_sql(self, cursor, company_data, fundamental_analysis_data, stock_data):
        execute_values(
            cursor,
            """
            INSERT INTO COMPANY_FUNDAMENTAL_ANALYSIS (
                stock_period, stock_profit, stock_loss, stock_cashin, stock_cashout,
                stock_debt, stock_expenditure, company_id
            ) VALUES %s
            """,
            [
                (
                    f["stock_period"],
                    f["stock_profit"],
                    f["stock_loss"],
                    f["stock_cashin"],
                    f["stock_cashout"],
                    f["stock_debt"],
                    f["stock_expenditure"],
                    f["company_id"],
                )
                for f in fundamental_analysis_data
            ],
        )

        # Insert into STOCK_DATA
        execute_values(
            cursor,
            """
            INSERT INTO STOCK_DATA (
                company_id, stock_date, open_price, close_price, high, low, adj_close, volume
            ) VALUES %s
            """,
            [
                (
                    s["company_id"],
                    s["stock_date"],
                    s["open_price"],
                    s["close_price"],
                    s["high"],
                    s["low"],
                    s["adj_close"],
                    s["volume"],
                )
                for s in stock_data
            ],
        )
    def insert_and_get_company_id(self, company_data):
        with self.db_connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT company_id FROM public.COMPANY_INFO WHERE company_market_id = %s
                """,
                (company_data["company_market_id"],)
            )
            result = cursor.fetchone()
            if result:
                return result[0]
            cursor.execute(
                """
                INSERT INTO COMPANY_INFO (company_name, company_market_id)
                VALUES (%s, %s)
                RETURNING company_id
                """,
                (company_data["company_name"], company_data["company_market_id"])
            )
            return cursor.fetchone()[0]

