from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.customer.model.service_fee import ServiceFee
from backend.app.customer.schema.service_fee import CreateServiceFeeParam, UpdateServiceFeeParam
from backend.utils.timezone import timezone


class CRUDServiceFee(CRUDPlus[ServiceFee]):
    async def get(self, db: AsyncSession, fee_id: int) -> ServiceFee | None:
        return await self.select_model_by_column(db, id=fee_id, deleted=0)

    async def get_by_enterprise(
        self, db: AsyncSession, enterprise_id: int | None = None, payment_status: str | None = None
    ) -> Sequence[ServiceFee]:
        filters: dict = {'deleted': 0}
        if enterprise_id is not None:
            filters['enterprise_id'] = enterprise_id
        if payment_status is not None:
            filters['payment_status'] = payment_status
        return await self.select_models_order(db, 'created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateServiceFeeParam) -> None:
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, fee_id: int, obj: UpdateServiceFeeParam) -> int:
        return await self.update_model_by_column(db, obj, id=fee_id, deleted=0)

    async def delete(self, db: AsyncSession, fee_id: int) -> int:
        return await self.delete_model_by_column(
            db, logical_deletion=True, deleted_flag_column='deleted',
            deleted_flag_value=self.model.id, deleted_at_column='deleted_time',
            deleted_at_factory=timezone.now(), id=fee_id, deleted=0,
        )


service_fee_dao: CRUDServiceFee = CRUDServiceFee(ServiceFee)
