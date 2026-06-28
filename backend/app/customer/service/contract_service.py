from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.customer.crud.crud_contract import contract_dao
from backend.app.customer.crud.crud_enterprise import enterprise_dao
from backend.app.customer.model.contract import Contract
from backend.app.customer.schema.contract import CreateContractParam, UpdateContractParam
from backend.common.exception import errors


class ContractService:
    """合同服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Contract:
        """
        获取合同详情

        :param db: 数据库会话
        :param pk: 合同 ID
        :return:
        """
        contract = await contract_dao.get(db, pk)
        if not contract:
            raise errors.NotFoundError(msg='合同不存在')
        return contract

    @staticmethod
    async def get_by_enterprise(
        *,
        db: AsyncSession,
        enterprise_id: int | None = None,
        contract_name: str | None = None,
    ) -> Sequence[Contract]:
        """
        获取某企业的合同列表

        :param db: 数据库会话
        :param enterprise_id: 企业 ID
        :param contract_name: 合同名称
        :return:
        """
        return await contract_dao.get_by_enterprise(db, enterprise_id, contract_name=contract_name)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateContractParam) -> None:
        """
        创建合同

        :param db: 数据库会话
        :param obj: 合同创建参数
        :return:
        """
        # 验证企业是否存在
        enterprise = await enterprise_dao.get(db, obj.enterprise_id)
        if not enterprise:
            raise errors.NotFoundError(msg='关联企业不存在')
        # 验证合同编号唯一性
        existing = await contract_dao.get_by_contract_no(db, obj.contract_no)
        if existing:
            raise errors.ConflictError(msg='合同编号已存在')
        await contract_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateContractParam) -> int:
        """
        更新合同

        :param db: 数据库会话
        :param pk: 合同 ID
        :param obj: 合同更新参数
        :return:
        """
        contract = await contract_dao.get(db, pk)
        if not contract:
            raise errors.NotFoundError(msg='合同不存在')
        if contract.contract_no != obj.contract_no:
            existing = await contract_dao.get_by_contract_no(db, obj.contract_no)
            if existing:
                raise errors.ConflictError(msg='合同编号已存在')
        count = await contract_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        """
        删除合同

        :param db: 数据库会话
        :param pk: 合同 ID
        :return:
        """
        contract = await contract_dao.get(db, pk)
        if not contract:
            raise errors.NotFoundError(msg='合同不存在')
        count = await contract_dao.delete(db, pk)
        return count


contract_service: ContractService = ContractService()
