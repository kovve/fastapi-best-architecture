from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.customer.model.contract import Contract
from backend.app.customer.schema.contract import CreateContractParam, UpdateContractParam
from backend.utils.timezone import timezone


class CRUDContract(CRUDPlus[Contract]):
    """合同数据库操作类"""

    async def get(self, db: AsyncSession, contract_id: int) -> Contract | None:
        """
        获取合同详情

        :param db: 数据库会话
        :param contract_id: 合同 ID
        :return:
        """
        return await self.select_model_by_column(db, id=contract_id, deleted=0)

    async def get_by_contract_no(self, db: AsyncSession, contract_no: str) -> Contract | None:
        """
        通过合同编号获取合同

        :param db: 数据库会话
        :param contract_no: 合同编号
        :return:
        """
        return await self.select_model_by_column(db, contract_no=contract_no, deleted=0)

    async def get_by_enterprise(
        self,
        db: AsyncSession,
        enterprise_id: int | None = None,
        contract_name: str | None = None,
    ) -> Sequence[Contract]:
        """
        获取合同列表（可选按企业筛选）

        :param db: 数据库会话
        :param enterprise_id: 企业 ID（为空时查询全部）
        :param contract_name: 合同名称（模糊搜索）
        :return:
        """
        filters: dict = {'deleted': 0}
        if enterprise_id is not None:
            filters['enterprise_id'] = enterprise_id
        if contract_name is not None:
            filters['contract_name__like'] = f'%{contract_name}%'

        return await self.select_models_order(db, 'created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateContractParam) -> None:
        """
        创建合同

        :param db: 数据库会话
        :param obj: 创建合同参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, contract_id: int, obj: UpdateContractParam) -> int:
        """
        更新合同

        :param db: 数据库会话
        :param contract_id: 合同 ID
        :param obj: 更新合同参数
        :return:
        """
        return await self.update_model_by_column(db, obj, id=contract_id, deleted=0)

    async def delete(self, db: AsyncSession, contract_id: int) -> int:
        """
        删除合同（逻辑删除）

        :param db: 数据库会话
        :param contract_id: 合同 ID
        :return:
        """
        return await self.delete_model_by_column(
            db,
            logical_deletion=True,
            deleted_flag_column='deleted',
            deleted_flag_value=self.model.id,
            deleted_at_column='deleted_time',
            deleted_at_factory=timezone.now(),
            id=contract_id,
            deleted=0,
        )


contract_dao: CRUDContract = CRUDContract(Contract)
