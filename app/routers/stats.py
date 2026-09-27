"""
Stats router

Endpoints with click statistics and the CSV report download.

@author adrianpmdev
"""

import sqlite3

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response

from app import reports, repository
from app.database import get_db
from app.schemas import DailyClicks, ProductClicks

router = APIRouter(tags=["Stats"])


@router.get("/stats/products", response_model=list[ProductClicks])
def clicks_by_product(db: sqlite3.Connection = Depends(get_db)):
    return reports.clicks_by_product(db)


@router.get("/stats/daily", response_model=list[DailyClicks])
def clicks_by_day(
    product_id: int | None = Query(default=None, gt=0),
    db: sqlite3.Connection = Depends(get_db),
):
    if product_id is not None and not repository.product_exists(db, product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return reports.clicks_by_day(db, product_id)


@router.get("/reports/clicks.csv")
def download_clicks_report(db: sqlite3.Connection = Depends(get_db)):
    csv_content = reports.clicks_report_csv(db)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="clicks_report.csv"'},
    )
