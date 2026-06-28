from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.customer.crud.crud_enterprise import enterprise_dao
from backend.app.customer.crud.crud_project_record import project_record_dao
from backend.app.customer.model.project_record import ProjectRecord
from backend.app.customer.schema.project_record import CreateProjectRecordParam, UpdateProjectRecordParam
from backend.common.exception import errors


class ProjectRecordService:
    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> ProjectRecord:
        data = await project_record_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='申报项目记录不存在')
        return data

    @staticmethod
    async def get_by_enterprise(
        *, db: AsyncSession, enterprise_id: int | None = None, project_name: str | None = None
    ) -> Sequence[ProjectRecord]:
        return await project_record_dao.get_by_enterprise(db, enterprise_id, project_name=project_name)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateProjectRecordParam) -> None:
        enterprise = await enterprise_dao.get(db, obj.enterprise_id)
        if not enterprise:
            raise errors.NotFoundError(msg='关联企业不存在')
        await project_record_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateProjectRecordParam) -> int:
        data = await project_record_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='申报项目记录不存在')
        return await project_record_dao.update(db, pk, obj)

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        data = await project_record_dao.get(db, pk)
        if not data:
            raise errors.NotFoundError(msg='申报项目记录不存在')
        return await project_record_dao.delete(db, pk)


project_record_service: ProjectRecordService = ProjectRecordService()
