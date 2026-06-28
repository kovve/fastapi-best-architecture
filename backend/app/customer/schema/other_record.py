from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class OtherRecordSchemaBase(SchemaBase):
    enterprise_id: int = Field(description='关联企业ID')
    record_type: str | None = Field(None, description='记录类型')
    title: str = Field(description='标题')
    content: str | None = Field(None, description='内容')
    record_date: str | None = Field(None, description='日期')
    file_path: str | None = Field(None, description='附件路径')


class CreateOtherRecordParam(OtherRecordSchemaBase):
    """创建其他记录参数"""


class UpdateOtherRecordParam(SchemaBase):
    record_type: str | None = Field(None, description='记录类型')
    title: str = Field(description='标题')
    content: str | None = Field(None, description='内容')
    record_date: str | None = Field(None, description='日期')
    file_path: str | None = Field(None, description='附件路径')


class GetOtherRecordDetail(OtherRecordSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description='ID')
    deleted: int = Field(description='是否已删除')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
    deleted_time: datetime | None = Field(None, description='删除时间')
