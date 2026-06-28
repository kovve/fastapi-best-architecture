from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.customer.crud.crud_enterprise import enterprise_dao
from backend.app.customer.crud.crud_patent import patent_dao
from backend.app.customer.model.patent import Patent
from backend.app.customer.schema.patent import CreatePatentParam, UpdatePatentParam
from backend.common.exception import errors


class PatentService:
    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Patent:
        data = await patent_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='专利不存在')
        return data

    @staticmethod
    async def get_by_enterprise(
        *, db: AsyncSession, enterprise_id: int | None = None, patent_name: str | None = None
    ) -> Sequence[Patent]:
        return await patent_dao.get_by_enterprise(db, enterprise_id, patent_name=patent_name)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreatePatentParam) -> None:
        enterprise = await enterprise_dao.get(db, obj.enterprise_id)
        if not enterprise:
            raise errors.NotFoundError(msg='关联企业不存在')
        await patent_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdatePatentParam) -> int:
        data = await patent_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='专利不存在')
        return await patent_dao.update(db, pk, obj)

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        data = await patent_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='专利不存在')
        return await patent_dao.delete(db, pk)


patent_service: PatentService = PatentService()
