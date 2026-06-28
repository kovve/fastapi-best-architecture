from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.customer.model.patent import Patent
from backend.app.customer.schema.patent import CreatePatentParam, UpdatePatentParam
from backend.utils.timezone import timezone


class CRUDPatent(CRUDPlus[Patent]):
    async def get(self, db: AsyncSession, patent_id: int) -> Patent | None:
        return await self.select_model_by_column(db, id=patent_id, deleted=0)

    async def get_by_enterprise(
        self, db: AsyncSession, enterprise_id: int | None = None, patent_name: str | None = None
    ) -> Sequence[Patent]:
        filters: dict = {'deleted': 0}
        if enterprise_id is not None:
            filters['enterprise_id'] = enterprise_id
        if patent_name is not None:
            filters['patent_name__like'] = f'%{patent_name}%'
        return await self.select_models_order(db, 'created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreatePatentParam) -> None:
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, patent_id: int, obj: UpdatePatentParam) -> int:
        return await self.update_model_by_column(db, obj, id=patent_id, deleted=0)

    async def delete(self, db: AsyncSession, patent_id: int) -> int:
        return await self.delete_model_by_column(
            db, logical_deletion=True, deleted_flag_column='deleted',
            deleted_flag_value=self.model.id, deleted_at_column='deleted_time',
            deleted_at_factory=timezone.now(), id=patent_id, deleted=0,
        )


patent_dao: CRUDPatent = CRUDPatent(Patent)
