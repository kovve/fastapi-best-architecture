from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.customer.crud.crud_enterprise import enterprise_dao
from backend.app.customer.crud.crud_financial_data import financial_data_dao
from backend.app.customer.model.financial_data import FinancialData
from backend.app.customer.schema.financial_data import CreateFinancialDataParam, UpdateFinancialDataParam
from backend.common.exception import errors


class FinancialDataService:
    """财务数据服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> FinancialData:
        """
        获取财务数据详情

        :param db: 数据库会话
        :param pk: 财务数据 ID
        :return:
        """
        data = await financial_data_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='财务数据不存在')
        return data

    @staticmethod
    async def get_by_enterprise(
        *,
        db: AsyncSession,
        enterprise_id: int | None = None,
        year: int | None = None,
    ) -> Sequence[FinancialData]:
        """
        获取某企业的财务数据列表

        :param db: 数据库会话
        :param enterprise_id: 企业 ID
        :param year: 财务年度
        :return:
        """
        return await financial_data_dao.get_by_enterprise(db, enterprise_id, year=year)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateFinancialDataParam) -> None:
        """
        创建财务数据

        :param db: 数据库会话
        :param obj: 财务数据创建参数
        :return:
        """
        # 验证企业是否存在
        enterprise = await enterprise_dao.get(db, obj.enterprise_id)
        if not enterprise:
            raise errors.NotFoundError(msg='关联企业不存在')
        # 验证同一企业同一年度唯一
        existing = await financial_data_dao.get_by_enterprise_and_year(db, obj.enterprise_id, obj.year)
        if existing:
            raise errors.ConflictError(msg='该企业该年度的财务数据已存在')
        await financial_data_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateFinancialDataParam) -> int:
        """
        更新财务数据

        :param db: 数据库会话
        :param pk: 财务数据 ID
        :param obj: 财务数据更新参数
        :return:
        """
        data = await financial_data_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='财务数据不存在')
        # 检查年度是否冲突（如果修改了年度）
        if data.year != obj.year:
            existing = await financial_data_dao.get_by_enterprise_and_year(db, data.enterprise_id, obj.year)
            if existing:
                raise errors.ConflictError(msg='该企业该年度的财务数据已存在')
        count = await financial_data_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        """
        删除财务数据

        :param db: 数据库会话
        :param pk: 财务数据 ID
        :return:
        """
        data = await financial_data_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='财务数据不存在')
        count = await financial_data_dao.delete(db, pk)
        return count


financial_data_service: FinancialDataService = FinancialDataService()
