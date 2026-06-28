from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.customer.model.financial_data import FinancialData
from backend.app.customer.schema.financial_data import CreateFinancialDataParam, UpdateFinancialDataParam
from backend.utils.timezone import timezone


class CRUDFinancialData(CRUDPlus[FinancialData]):
    """财务数据数据库操作类"""

    async def get(self, db: AsyncSession, financial_id: int) -> FinancialData | None:
        """
        获取财务数据详情

        :param db: 数据库会话
        :param financial_id: 财务数据 ID
        :return:
        """
        return await self.select_model_by_column(db, id=financial_id, deleted=0)

    async def get_by_enterprise_and_year(
        self, db: AsyncSession, enterprise_id: int, year: int
    ) -> FinancialData | None:
        """
        通过企业ID和年份获取财务数据

        :param db: 数据库会话
        :param enterprise_id: 企业 ID
        :param year: 财务年度
        :return:
        """
        return await self.select_model_by_column(db, enterprise_id=enterprise_id, year=year, deleted=0)

    async def get_by_enterprise(
        self,
        db: AsyncSession,
        enterprise_id: int | None = None,
        year: int | None = None,
    ) -> Sequence[FinancialData]:
        filters: dict = {'deleted': 0}
        if enterprise_id is not None:
            filters['enterprise_id'] = enterprise_id
        if year is not None:
            filters['year'] = year

        return await self.select_models_order(db, 'year', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateFinancialDataParam) -> None:
        """
        创建财务数据

        :param db: 数据库会话
        :param obj: 创建财务数据参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, financial_id: int, obj: UpdateFinancialDataParam) -> int:
        """
        更新财务数据

        :param db: 数据库会话
        :param financial_id: 财务数据 ID
        :param obj: 更新财务数据参数
        :return:
        """
        return await self.update_model_by_column(db, obj, id=financial_id, deleted=0)

    async def delete(self, db: AsyncSession, financial_id: int) -> int:
        """
        删除财务数据（逻辑删除）

        :param db: 数据库会话
        :param financial_id: 财务数据 ID
        :return:
        """
        return await self.delete_model_by_column(
            db,
            logical_deletion=True,
            deleted_flag_column='deleted',
            deleted_flag_value=self.model.id,
            deleted_at_column='deleted_time',
            deleted_at_factory=timezone.now(),
            id=financial_id,
            deleted=0,
        )


financial_data_dao: CRUDFinancialData = CRUDFinancialData(FinancialData)
