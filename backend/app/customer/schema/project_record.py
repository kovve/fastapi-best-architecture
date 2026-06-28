from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class ProjectRecordSchemaBase(SchemaBase):
    enterprise_id: int = Field(description='关联企业ID')
    project_name: str = Field(description='项目名称')
    project_type: str | None = Field(None, description='项目类型')
    declaration_date: str | None = Field(None, description='申报日期')
    declaration_amount: float | None = Field(None, description='申报金额')
    approved_amount: float | None = Field(None, description='批准金额')
    status: str | None = Field(None, description='状态')
    declaration_department: str | None = Field(None, description='申报部门/机构')
    remarks: str | None = Field(None, description='备注')


class CreateProjectRecordParam(ProjectRecordSchemaBase):
    """创建申报项目参数"""


class UpdateProjectRecordParam(SchemaBase):
    project_name: str = Field(description='项目名称')
    project_type: str | None = Field(None, description='项目类型')
    declaration_date: str | None = Field(None, description='申报日期')
    declaration_amount: float | None = Field(None, description='申报金额')
    approved_amount: float | None = Field(None, description='批准金额')
    status: str | None = Field(None, description='状态')
    declaration_department: str | None = Field(None, description='申报部门/机构')
    remarks: str | None = Field(None, description='备注')


class GetProjectRecordDetail(ProjectRecordSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description='ID')
    deleted: int = Field(description='是否已删除')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
    deleted_time: datetime | None = Field(None, description='删除时间')
