"""
Schemas

Pydantic models used to validate requests and shape API responses.

@author adrianpmdev
"""

from datetime import date, datetime

from pydantic import BaseModel, Field


class ClickCreate(BaseModel):
    product_id: int = Field(gt=0)


class ClickRead(BaseModel):
    id: int
    product_id: int
    clicked_at: datetime


class ProductClicks(BaseModel):
    product_id: int
    name: str
    total_clicks: int


class DailyClicks(BaseModel):
    date: date
    total_clicks: int
