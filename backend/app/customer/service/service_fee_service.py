from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.customer.crud.crud_enterprise import enterprise_dao
from backend.app.customer.crud.crud_service_fee import service_fee_dao
from backend.app.customer.model.service_fee import ServiceFee
from backend.app.customer.schema.service_fee import CreateServiceFeeParam, UpdateServiceFeeParam
from backend.common.exception import errors


class ServiceFeeService:
    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> ServiceFee:
        data = await service_fee_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='服务费记录不存在')
        return data

    @staticmethod
    async def get_by_enterprise(
        *, db: AsyncSession, enterprise_id: int | None = None, payment_status: str | None = None
    ) -> Sequence[ServiceFee]:
        return await service_fee_dao.get_by_enterprise(db, enterprise_id, payment_status=payment_status)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateServiceFeeParam) -> None:
        enterprise = await enterprise_dao.get(db, obj.enterprise_id)
        if not enterprise:
            raise errors.NotFoundError(msg='关联企业不存在')
        await service_fee_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateServiceFeeParam) -> int:
        data = await service_fee_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='服务费记录不存在')
        return await service_fee_dao.update(db, pk, obj)

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        data = await service_fee_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='服务费记录不存在')
        return await service_fee_dao.delete(db, pk)


service_fee_service: ServiceFeeService = ServiceFeeService()
