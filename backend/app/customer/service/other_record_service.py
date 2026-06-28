from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.customer.crud.crud_enterprise import enterprise_dao
from backend.app.customer.crud.crud_other_record import other_record_dao
from backend.app.customer.model.other_record import OtherRecord
from backend.app.customer.schema.other_record import CreateOtherRecordParam, UpdateOtherRecordParam
from backend.common.exception import errors


class OtherRecordService:
    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> OtherRecord:
        data = await other_record_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='记录不存在')
        return data

    @staticmethod
    async def get_by_enterprise(
        *, db: AsyncSession, enterprise_id: int | None = None, record_type: str | None = None, title: str | None = None
    ) -> Sequence[OtherRecord]:
        return await other_record_dao.get_by_enterprise(db, enterprise_id, record_type=record_type, title=title)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateOtherRecordParam) -> None:
        enterprise = await enterprise_dao.get(db, obj.enterprise_id)
        if not enterprise:
            raise errors.NotFoundError(msg='关联企业不存在')
        await other_record_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateOtherRecordParam) -> int:
        data = await other_record_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='记录不存在')
        return await other_record_dao.update(db, pk, obj)

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        data = await other_record_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='记录不存在')
        return await other_record_dao.delete(db, pk)


other_record_service: OtherRecordService = OtherRecordService()
