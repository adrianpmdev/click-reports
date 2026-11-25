"""
Stats router

Endpoints with click statistics and the CSV report download.

@author adrianpmdev
"""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import Response

from app import reports, repository
from app.database import DbDep
from app.schemas import DailyClicks, ProductClicks

router = APIRouter(tags=["Stats"])


@router.get("/stats/products", response_model=list[ProductClicks])
def clicks_by_product(db: DbDep):
    """Total clicks per product, most clicked first."""
    return repository.count_clicks_by_product(db)


@router.get("/stats/daily", response_model=list[DailyClicks])
def clicks_by_day(db: DbDep, product_id: Annotated[int | None, Query(gt=0)] = None):
    """Total clicks per UTC day, for every product or only for one."""
    if product_id is not None and not repository.product_exists(db, product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return repository.count_clicks_by_day(db, product_id)


@router.get("/reports/clicks.csv")
def download_clicks_report(db: DbDep):
    """Download a CSV with the clicks per day and product."""
    return Response(
        content=reports.clicks_report_csv(db),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="clicks_report.csv"'},
    )
