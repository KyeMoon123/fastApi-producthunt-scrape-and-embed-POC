from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from db.models.dummy_model import DummyModel
from db.models.source_system import SourceSystem


class SourceSystemDAO:
    """Class for accessing dummy table."""

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def create_source(self, name: str) -> None:
        """
        Add single dummy to session.

        :param name: name of a dummy.
        """
        self.session.add(SourceSystem(system_name=name))

    async def get_all_dummies(self, limit: int, offset: int) -> List[DummyModel]:
        """
        Get all dummy models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_dummies = await self.session.execute(
            select(DummyModel).limit(limit).offset(offset),
        )

        return raw_dummies.scalars().fetchall()

    async def find_by_system_name(self, system_name: str) -> SourceSystem:
        """
        Get all dummy models with limit/offset pagination.
        :param system_name: limit of dummies.
        :return: stream of dummies.
        """
        system = await self.session.execute(
            select(SourceSystem).filter_by(system_name=system_name),
        )
        return 1

    async def filter(
            self,
            name: Optional[str] = None,
    ) -> List[DummyModel]:
        """
        Get specific dummy model.

        :param name: name of dummy instance.
        :return: dummy models.
        """
        query = select(DummyModel)
        if name:
            query = query.where(DummyModel.name == name)
        rows = await self.session.execute(query)
        return rows.scalars().fetchall()
