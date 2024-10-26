from fastapi import APIRouter, Depends
from typing import List
from app.search.schemas import FilterParams, SClientSearch
from app.users.dependencies import get_current_client
from app.users.dao import ClientsDAO

router = APIRouter(
    prefix="/list",
    tags=["Search clients by filters"]
)


@router.get("")
async def list_clients(
        filters: FilterParams = Depends(),
        current_client=Depends(get_current_client)
) -> List[SClientSearch]:
    clients = await ClientsDAO.list_clients(filters, current_client.id, current_client.lat, current_client.lon)
    return clients
