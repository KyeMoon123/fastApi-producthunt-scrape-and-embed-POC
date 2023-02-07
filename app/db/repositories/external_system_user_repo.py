from typing import List, Optional, Any

from fastapi import Depends
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from db.models.dummy_model import DummyModel
from db.models.external_system_user_details import ExternalSystemUserDetailsModel


class ExternalSystemUserDetailsDAO:
    """Class for accessing dummy table."""

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def create_source(self, name: str) -> None:
        """
        Add single dummy to session.

        :param name: name of a dummy.
        """
        self.session.add(ExternalSystemUserDetailsModel(system_name=name))

    async def find_by_external_id(self, external_id: str) -> Result[ExternalSystemUserDetailsModel]:
        query = select(ExternalSystemUserDetailsModel).where(ExternalSystemUserDetailsModel.external_id == external_id)
        result = await self.session.execute(query)
        return result
