from fastapi import APIRouter

from . import cmc_client

router = APIRouter(
    prefix='/cryptocurrency',
)

@router.get('')
async def get_cryptocurrency():
    return await cmc_client.get_listings()

@router.get('/{current_id}')
async def get_cryptocurrency_by_id(current_id: int):
    return await cmc_client.get_currency(current_id)