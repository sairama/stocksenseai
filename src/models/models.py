from pydantic import BaseModel, ValidationError, validator


class StockInsertRequest(BaseModel):
    stock_name: str
    stock_id: str
    total_days: int
    stock_interval: str = None

    @validator("stock_interval", pre=True, always=True)
    def validate_stock_interval(cls, value):
        import re
        if value is not None:
            # Regex to validate the pattern
            pattern = r"^\d+(m|h|d|wk|mo)$"
            if not re.match(pattern, value):
                raise ValueError(
                    "Invalid stock_interval. It must be a number followed by one of the units: "
                    "'m' (minutes), 'h' (hours), 'd' (days), 'wk' (weeks), or 'mo' (months)."
                )
        return value
