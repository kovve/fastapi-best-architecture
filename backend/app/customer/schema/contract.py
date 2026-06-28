from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class ContractSchemaBase(SchemaBase):
    """合同基础模型"""

    enterprise_id: int = Field(description='关联企业ID')
    contract_no: str = Field(description='合同编号')
    contract_name: str = Field(description='合同名称')
    contract_type: str | None = Field(None, description='合同类型')
    sign_date: str | None = Field(None, description='签订日期')
    start_date: str | None = Field(None, description='开始日期')
    end_date: str | None = Field(None, description='结束日期')
    amount: float | None = Field(None, description='合同金额')
    our_party: str | None = Field(None, description='我方签约主体')
    counter_party: str | None = Field(None, description='对方签约主体')
    status: StatusType = Field(description='状态')
    file_path: str | None = Field(None, description='合同文件路径')
    remarks: str | None = Field(None, description='备注')


class CreateContractParam(ContractSchemaBase):
    """创建合同参数"""


class UpdateContractParam(SchemaBase):
    """更新合同参数"""

    contract_no: str = Field(description='合同编号')
    contract_name: str = Field(description='合同名称')
    contract_type: str | None = Field(None, description='合同类型')
    sign_date: str | None = Field(None, description='签订日期')
    start_date: str | None = Field(None, description='开始日期')
    end_date: str | None = Field(None, description='结束日期')
    amount: float | None = Field(None, description='合同金额')
    our_party: str | None = Field(None, description='我方签约主体')
    counter_party: str | None = Field(None, description='对方签约主体')
    status: StatusType = Field(description='状态')
    file_path: str | None = Field(None, description='合同文件路径')
    remarks: str | None = Field(None, description='备注')


class GetContractDetail(ContractSchemaBase):
    """合同详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='合同 ID')
    deleted: int = Field(description='是否已删除')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
    deleted_time: datetime | None = Field(None, description='删除时间')
