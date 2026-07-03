from typing import Annotated
from fastapi import APIRouter, Depends, File
from sqlalchemy.ext.asyncio import AsyncSession

from ...deps.db import get_db
from ....schemas.data_loader import LoadDataRequest, LoadDataResponse
from ....services import data_loader as data_loader_service

router = APIRouter(prefix='/load-data')

@router.post('', response_model=LoadDataResponse, description='Load the CSV data in the DB')
async def load_data(load_data: Annotated[LoadDataRequest, File()], db: AsyncSession = Depends(get_db)):
    return await data_loader_service.load_data(db, load_data)
