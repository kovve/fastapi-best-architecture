from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.customer.model.project_record import ProjectRecord
from backend.app.customer.schema.project_record import CreateProjectRecordParam, UpdateProjectRecordParam
from backend.utils.timezone import timezone


class CRUDProjectRecord(CRUDPlus[ProjectRecord]):
    async def get(self, db: AsyncSession, record_id: int) -> ProjectRecord | None:
        return await self.select_model_by_column(db, id=record_id, deleted=0)

    async def get_by_enterprise(
        self, db: AsyncSession, enterprise_id: int | None = None, project_name: str | None = None
    ) -> Sequence[ProjectRecord]:
        filters: dict = {'deleted': 0}
        if enterprise_id is not None:
            filters['enterprise_id'] = enterprise_id
        if project_name is not None:
            filters['project_name__like'] = f'%{project_name}%'
        return await self.select_models_order(db, 'created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateProjectRecordParam) -> None:
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, record_id: int, obj: UpdateProjectRecordParam) -> int:
        return await self.update_model_by_column(db, obj, id=record_id, deleted=0)

    async def delete(self, db: AsyncSession, record_id: int) -> int:
        return await self.delete_model_by_column(
            db, logical_deletion=True, deleted_flag_column='deleted',
            deleted_flag_value=self.model.id, deleted_at_column='deleted_time',
            deleted_at_factory=timezone.now(), id=record_id, deleted=0,
        )


project_record_dao: CRUDProjectRecord = CRUDProjectRecord(ProjectRecord)
