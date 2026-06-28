from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import CustomEmailStr, CustomPhoneNumber, SchemaBase


class EnterpriseSchemaBase(SchemaBase):
    """企业基础模型"""

    name: str = Field(description='企业名称')
    short_name: str | None = Field(None, description='简称')
    unified_social_credit_code: str | None = Field(None, description='统一社会信用代码')
    legal_representative: str | None = Field(None, description='法定代表人')
    registered_address: str | None = Field(None, description='注册地址')
    business_scope: str | None = Field(None, description='经营范围')
    registered_capital: str | None = Field(None, description='注册资本')
    establishment_date: str | None = Field(None, description='成立日期')
    industry: str | None = Field(None, description='所属行业')
    enterprise_type: str | None = Field(None, description='企业类型')
    contact_person: str | None = Field(None, description='联系人')
    contact_phone: CustomPhoneNumber | None = Field(None, description='联系电话')
    contact_email: CustomEmailStr | None = Field(None, description='联系邮箱')
    status: StatusType = Field(description='状态')
    remarks: str | None = Field(None, description='备注')


class CreateEnterpriseParam(EnterpriseSchemaBase):
    """创建企业参数"""


class UpdateEnterpriseParam(EnterpriseSchemaBase):
    """更新企业参数"""


class GetEnterpriseDetail(EnterpriseSchemaBase):
    """企业详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='企业 ID')
    deleted: int = Field(description='是否已删除（0：否；id：是）')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
    deleted_time: datetime | None = Field(None, description='删除时间')
