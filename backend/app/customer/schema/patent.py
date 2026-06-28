from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class PatentSchemaBase(SchemaBase):
    enterprise_id: int = Field(description='关联企业ID')
    patent_name: str = Field(description='专利名称')
    patent_no: str | None = Field(None, description='专利号')
    patent_type: str | None = Field(None, description='类型(发明/实用新型/外观设计)')
    application_no: str | None = Field(None, description='申请号')
    application_date: str | None = Field(None, description='申请日期')
    publication_date: str | None = Field(None, description='公开日期')
    authorization_date: str | None = Field(None, description='授权日期')
    patentee: str | None = Field(None, description='专利权人')
    inventor: str | None = Field(None, description='发明人')
    legal_status: str | None = Field(None, description='法律状态')
    remarks: str | None = Field(None, description='备注')


class CreatePatentParam(PatentSchemaBase):
    """创建专利参数"""


class UpdatePatentParam(SchemaBase):
    patent_name: str = Field(description='专利名称')
    patent_no: str | None = Field(None, description='专利号')
    patent_type: str | None = Field(None, description='类型')
    application_no: str | None = Field(None, description='申请号')
    application_date: str | None = Field(None, description='申请日期')
    publication_date: str | None = Field(None, description='公开日期')
    authorization_date: str | None = Field(None, description='授权日期')
    patentee: str | None = Field(None, description='专利权人')
    inventor: str | None = Field(None, description='发明人')
    legal_status: str | None = Field(None, description='法律状态')
    remarks: str | None = Field(None, description='备注')


class GetPatentDetail(PatentSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description='ID')
    deleted: int = Field(description='是否已删除')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
    deleted_time: datetime | None = Field(None, description='删除时间')
