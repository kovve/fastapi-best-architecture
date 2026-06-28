from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class ServiceFeeSchemaBase(SchemaBase):
    enterprise_id: int = Field(description='关联企业ID')
    fee_type: str | None = Field(None, description='费用类型')
    amount: float | None = Field(None, description='金额')
    receivable_date: str | None = Field(None, description='应收日期')
    received_date: str | None = Field(None, description='实收日期')
    payment_status: str | None = Field(None, description='收款状态')
    invoice_no: str | None = Field(None, description='发票号')
    invoice_date: str | None = Field(None, description='开票日期')
    remarks: str | None = Field(None, description='备注')


class CreateServiceFeeParam(ServiceFeeSchemaBase):
    """创建服务费参数"""


class UpdateServiceFeeParam(SchemaBase):
    fee_type: str | None = Field(None, description='费用类型')
    amount: float | None = Field(None, description='金额')
    receivable_date: str | None = Field(None, description='应收日期')
    received_date: str | None = Field(None, description='实收日期')
    payment_status: str | None = Field(None, description='收款状态')
    invoice_no: str | None = Field(None, description='发票号')
    invoice_date: str | None = Field(None, description='开票日期')
    remarks: str | None = Field(None, description='备注')


class GetServiceFeeDetail(ServiceFeeSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description='ID')
    deleted: int = Field(description='是否已删除')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
    deleted_time: datetime | None = Field(None, description='删除时间')
