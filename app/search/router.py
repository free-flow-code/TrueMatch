from fastapi import APIRouter, Depends
from typing import List
from app.search.schemas import FilterParams, SClientSearch
from app.users.dao import ClientsDAO

router = APIRouter(
    prefix="/list",
    tags=["Search clients by filters"]
)


@router.get("")
async def list_clients(filters: FilterParams = Depends()) -> List[SClientSearch]:
    clients = await ClientsDAO.list_clients(filters)
    return clients
