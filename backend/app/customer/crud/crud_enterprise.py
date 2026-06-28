from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.customer.model.enterprise import Enterprise
from backend.app.customer.schema.enterprise import CreateEnterpriseParam, UpdateEnterpriseParam
from backend.utils.timezone import timezone


class CRUDEnterprise(CRUDPlus[Enterprise]):
    """企业数据库操作类"""

    async def get(self, db: AsyncSession, enterprise_id: int) -> Enterprise | None:
        """
        获取企业详情

        :param db: 数据库会话
        :param enterprise_id: 企业 ID
        :return:
        """
        return await self.select_model_by_column(db, id=enterprise_id, deleted=0)

    async def get_by_name(self, db: AsyncSession, name: str) -> Enterprise | None:
        """
        通过名称获取企业

        :param db: 数据库会话
        :param name: 企业名称
        :return:
        """
        return await self.select_model_by_column(db, name=name, deleted=0)

    async def get_all(
        self,
        db: AsyncSession,
        name: str | None = None,
        credit_code: str | None = None,
        status: int | None = None,
    ) -> Sequence[Enterprise]:
        """
        获取所有企业

        :param db: 数据库会话
        :param name: 企业名称（模糊搜索）
        :param credit_code: 统一社会信用代码
        :param status: 状态
        :return:
        """
        filters: dict = {'deleted': 0}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if credit_code is not None:
            filters['unified_social_credit_code__like'] = f'%{credit_code}%'
        if status is not None:
            filters['status'] = status

        return await self.select_models_order(db, 'created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateEnterpriseParam) -> None:
        """
        创建企业

        :param db: 数据库会话
        :param obj: 创建企业参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, enterprise_id: int, obj: UpdateEnterpriseParam) -> int:
        """
        更新企业

        :param db: 数据库会话
        :param enterprise_id: 企业 ID
        :param obj: 更新企业参数
        :return:
        """
        return await self.update_model_by_column(db, obj, id=enterprise_id, deleted=0)

    async def delete(self, db: AsyncSession, enterprise_id: int) -> int:
        """
        删除企业（逻辑删除）

        :param db: 数据库会话
        :param enterprise_id: 企业 ID
        :return:
        """
        return await self.delete_model_by_column(
            db,
            logical_deletion=True,
            deleted_flag_column='deleted',
            deleted_flag_value=self.model.id,
            deleted_at_column='deleted_time',
            deleted_at_factory=timezone.now(),
            id=enterprise_id,
            deleted=0,
        )


enterprise_dao: CRUDEnterprise = CRUDEnterprise(Enterprise)
