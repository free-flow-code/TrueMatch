from app.dao.base import BaseDAO
from app.users.models import Clients


class ClientsDAO(BaseDAO):
    model = Clients
