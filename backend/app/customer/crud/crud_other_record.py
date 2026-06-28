from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.customer.model.other_record import OtherRecord
from backend.app.customer.schema.other_record import CreateOtherRecordParam, UpdateOtherRecordParam
from backend.utils.timezone import timezone


class CRUDOtherRecord(CRUDPlus[OtherRecord]):
    async def get(self, db: AsyncSession, record_id: int) -> OtherRecord | None:
        return await self.select_model_by_column(db, id=record_id, deleted=0)

    async def get_by_enterprise(
        self, db: AsyncSession, enterprise_id: int | None = None, record_type: str | None = None, title: str | None = None
    ) -> Sequence[OtherRecord]:
        filters: dict = {'deleted': 0}
        if enterprise_id is not None:
            filters['enterprise_id'] = enterprise_id
        if record_type is not None:
            filters['record_type'] = record_type
        if title is not None:
            filters['title__like'] = f'%{title}%'
        return await self.select_models_order(db, 'created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateOtherRecordParam) -> None:
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, record_id: int, obj: UpdateOtherRecordParam) -> int:
        return await self.update_model_by_column(db, obj, id=record_id, deleted=0)

    async def delete(self, db: AsyncSession, record_id: int) -> int:
        return await self.delete_model_by_column(
            db, logical_deletion=True, deleted_flag_column='deleted',
            deleted_flag_value=self.model.id, deleted_at_column='deleted_time',
            deleted_at_factory=timezone.now(), id=record_id, deleted=0,
        )


other_record_dao: CRUDOtherRecord = CRUDOtherRecord(OtherRecord)
