"""
Clicks router

Endpoint to register a click on a product.

@author adrianpmdev
"""

from fastapi import APIRouter, HTTPException, status

from app import repository
from app.database import DbDep
from app.schemas import ClickCreate, ClickRead

router = APIRouter(prefix="/clicks", tags=["Clicks"])


@router.post("", response_model=ClickRead, status_code=status.HTTP_201_CREATED)
def register_click(payload: ClickCreate, db: DbDep):
    """Register a click on a product."""
    if not repository.product_exists(db, payload.product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return repository.create_click(db, payload.product_id)
