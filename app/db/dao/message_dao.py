from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from db.models.message_model import MessageModel


class MessageDAO:
    """Class for accessing dummy table."""

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def create_dummy_model(self, name: str) -> None:
        """
        Add single dummy to session.

        :param name: name of a dummy.
        """
        self.session.add(MessageModel())

    async def get_all_dummies(self, limit: int, offset: int) -> List[MessageModel]:
        """
        Get all dummy models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_dummies = await self.session.execute(
            select(MessageModel).limit(limit).offset(offset),
        )

        return raw_dummies.scalars().fetchall()

    async def filter(
        self,
        name: Optional[str] = None,
    ) -> List[MessageModel]:
        """
        Get specific dummy model.

        :param name: name of dummy instance.
        :return: dummy models.
        """
        query = select(MessageModel)
        if name:
            query = query.where(MessageModel.name == name)
        rows = await self.session.execute(query)
        return rows.scalars().fetchall()
