from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.database import get_db
from db.models.mention_model import MentionModel
from db.models.mention_model import MentionModel


class MentionDAO:
    """Class for accessing dummy table."""

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session



    async def get_all_dummies(self, limit: int, offset: int) -> List[MentionModel]:
        """
        Get all dummy models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_dummies = await self.session.execute(
            select(MentionModel).limit(limit).offset(offset),
        )

        return raw_dummies.scalars().fetchall()

    async def filter(
            self,
            name: Optional[str] = None,
    ) -> List[MentionModel]:
        """
        Get specific dummy model.

        :param name: name of dummy instance.
        :return: dummy models.
        """
        query = select(MentionModel)
        if name:
            query = query.where(MentionModel.name == name)
        rows = await self.session.execute(query)
        return rows.scalars().fetchall()
