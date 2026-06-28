from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.customer.crud.crud_enterprise import enterprise_dao
from backend.app.customer.model.enterprise import Enterprise
from backend.app.customer.schema.enterprise import CreateEnterpriseParam, UpdateEnterpriseParam
from backend.common.exception import errors


class EnterpriseService:
    """企业服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Enterprise:
        """
        获取企业详情

        :param db: 数据库会话
        :param pk: 企业 ID
        :return:
        """
        enterprise = await enterprise_dao.get(db, pk)
        if not enterprise:
            raise errors.NotFoundError(msg='企业不存在')
        return enterprise

    @staticmethod
    async def get_all(
        *,
        db: AsyncSession,
        name: str | None = None,
        credit_code: str | None = None,
        status: int | None = None,
    ) -> Sequence[Enterprise]:
        """
        获取所有企业

        :param db: 数据库会话
        :param name: 企业名称
        :param credit_code: 统一社会信用代码
        :param status: 状态
        :return:
        """
        return await enterprise_dao.get_all(db, name=name, credit_code=credit_code, status=status)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateEnterpriseParam) -> None:
        """
        创建企业

        :param db: 数据库会话
        :param obj: 企业创建参数
        :return:
        """
        enterprise = await enterprise_dao.get_by_name(db, obj.name)
        if enterprise:
            raise errors.ConflictError(msg='企业名称已存在')
        await enterprise_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateEnterpriseParam) -> int:
        """
        更新企业

        :param db: 数据库会话
        :param pk: 企业 ID
        :param obj: 企业更新参数
        :return:
        """
        enterprise = await enterprise_dao.get(db, pk)
        if not enterprise:
            raise errors.NotFoundError(msg='企业不存在')
        if enterprise.name != obj.name:
            existing = await enterprise_dao.get_by_name(db, obj.name)
            if existing:
                raise errors.ConflictError(msg='企业名称已存在')
        count = await enterprise_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        """
        删除企业

        :param db: 数据库会话
        :param pk: 企业 ID
        :return:
        """
        enterprise = await enterprise_dao.get(db, pk)
        if not enterprise:
            raise errors.NotFoundError(msg='企业不存在')
        count = await enterprise_dao.delete(db, pk)
        return count


enterprise_service: EnterpriseService = EnterpriseService()
