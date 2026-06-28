from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class FinancialDataSchemaBase(SchemaBase):
    """财务数据基础模型"""

    enterprise_id: int = Field(description='关联企业ID')
    year: int = Field(description='财务年度')
    audit_status: str | None = Field(None, description='审计状态(已审计/未审计)')

    # 资产负债表 - 流动资产
    monetary_funds: float | None = Field(None, description='货币资金')
    accounts_receivable: float | None = Field(None, description='应收账款')
    prepayments: float | None = Field(None, description='预付账款')
    other_receivables: float | None = Field(None, description='其他应收款')
    inventory: float | None = Field(None, description='存货')
    current_assets_total: float | None = Field(None, description='流动资产合计')

    # 资产负债表 - 非流动资产
    fixed_assets_original: float | None = Field(None, description='固定资产原值')
    accumulated_depreciation: float | None = Field(None, description='累计折旧')
    fixed_assets_net: float | None = Field(None, description='固定资产净值')
    construction_in_progress: float | None = Field(None, description='在建工程')
    intangible_assets: float | None = Field(None, description='无形资产')
    non_current_assets_total: float | None = Field(None, description='非流动资产合计')

    # 资产总计
    total_assets: float | None = Field(None, description='资产总计')

    # 资产负债表 - 流动负债
    short_term_borrowings: float | None = Field(None, description='短期借款')
    accounts_payable: float | None = Field(None, description='应付账款')
    advance_receipts: float | None = Field(None, description='预收账款')
    employee_payables: float | None = Field(None, description='应付职工薪酬')
    taxes_payable: float | None = Field(None, description='应交税费')
    other_payables: float | None = Field(None, description='其他应付款')
    current_liabilities_total: float | None = Field(None, description='流动负债合计')

    # 资产负债表 - 非流动负债
    long_term_borrowings: float | None = Field(None, description='长期借款')
    long_term_payables: float | None = Field(None, description='长期应付款')
    non_current_liabilities_total: float | None = Field(None, description='非流动负债合计')

    # 负债合计
    total_liabilities: float | None = Field(None, description='负债合计')

    # 资产负债表 - 所有者权益
    paid_in_capital: float | None = Field(None, description='实收资本')
    capital_reserve: float | None = Field(None, description='资本公积')
    surplus_reserve: float | None = Field(None, description='盈余公积')
    undistributed_profit: float | None = Field(None, description='未分配利润')
    owners_equity_total: float | None = Field(None, description='所有者权益合计')

    # 利润表
    revenue: float | None = Field(None, description='营业收入')
    cost_of_sales: float | None = Field(None, description='营业成本')
    sales_tax_surcharge: float | None = Field(None, description='税金及附加')
    selling_expenses: float | None = Field(None, description='销售费用')
    administrative_expenses: float | None = Field(None, description='管理费用')
    financial_expenses: float | None = Field(None, description='财务费用')
    operating_profit: float | None = Field(None, description='营业利润')
    non_operating_income: float | None = Field(None, description='营业外收入')
    non_operating_expense: float | None = Field(None, description='营业外支出')
    total_profit: float | None = Field(None, description='利润总额')
    income_tax_expense: float | None = Field(None, description='所得税费用')
    net_profit: float | None = Field(None, description='净利润')

    # 现金流量表
    operating_cash_inflow: float | None = Field(None, description='经营活动现金流入')
    operating_cash_outflow: float | None = Field(None, description='经营活动现金流出')
    net_operating_cash_flow: float | None = Field(None, description='经营活动现金流量净额')
    investing_cash_inflow: float | None = Field(None, description='投资活动现金流入')
    investing_cash_outflow: float | None = Field(None, description='投资活动现金流出')
    net_investing_cash_flow: float | None = Field(None, description='投资活动现金流量净额')
    financing_cash_inflow: float | None = Field(None, description='筹资活动现金流入')
    financing_cash_outflow: float | None = Field(None, description='筹资活动现金流出')
    net_financing_cash_flow: float | None = Field(None, description='筹资活动现金流量净额')
    net_cash_flow: float | None = Field(None, description='现金及现金等价物净增加额')
    beginning_cash_balance: float | None = Field(None, description='期初现金及现金等价物余额')
    ending_cash_balance: float | None = Field(None, description='期末现金及现金等价物余额')

    remarks: str | None = Field(None, description='备注')


class CreateFinancialDataParam(FinancialDataSchemaBase):
    """创建财务数据参数"""


class UpdateFinancialDataParam(SchemaBase):
    """更新财务数据参数"""

    year: int = Field(description='财务年度')
    audit_status: str | None = Field(None, description='审计状态')

    monetary_funds: float | None = Field(None, description='货币资金')
    accounts_receivable: float | None = Field(None, description='应收账款')
    prepayments: float | None = Field(None, description='预付账款')
    other_receivables: float | None = Field(None, description='其他应收款')
    inventory: float | None = Field(None, description='存货')
    current_assets_total: float | None = Field(None, description='流动资产合计')
    fixed_assets_original: float | None = Field(None, description='固定资产原值')
    accumulated_depreciation: float | None = Field(None, description='累计折旧')
    fixed_assets_net: float | None = Field(None, description='固定资产净值')
    construction_in_progress: float | None = Field(None, description='在建工程')
    intangible_assets: float | None = Field(None, description='无形资产')
    non_current_assets_total: float | None = Field(None, description='非流动资产合计')
    total_assets: float | None = Field(None, description='资产总计')
    short_term_borrowings: float | None = Field(None, description='短期借款')
    accounts_payable: float | None = Field(None, description='应付账款')
    advance_receipts: float | None = Field(None, description='预收账款')
    employee_payables: float | None = Field(None, description='应付职工薪酬')
    taxes_payable: float | None = Field(None, description='应交税费')
    other_payables: float | None = Field(None, description='其他应付款')
    current_liabilities_total: float | None = Field(None, description='流动负债合计')
    long_term_borrowings: float | None = Field(None, description='长期借款')
    long_term_payables: float | None = Field(None, description='长期应付款')
    non_current_liabilities_total: float | None = Field(None, description='非流动负债合计')
    total_liabilities: float | None = Field(None, description='负债合计')
    paid_in_capital: float | None = Field(None, description='实收资本')
    capital_reserve: float | None = Field(None, description='资本公积')
    surplus_reserve: float | None = Field(None, description='盈余公积')
    undistributed_profit: float | None = Field(None, description='未分配利润')
    owners_equity_total: float | None = Field(None, description='所有者权益合计')
    revenue: float | None = Field(None, description='营业收入')
    cost_of_sales: float | None = Field(None, description='营业成本')
    sales_tax_surcharge: float | None = Field(None, description='税金及附加')
    selling_expenses: float | None = Field(None, description='销售费用')
    administrative_expenses: float | None = Field(None, description='管理费用')
    financial_expenses: float | None = Field(None, description='财务费用')
    operating_profit: float | None = Field(None, description='营业利润')
    non_operating_income: float | None = Field(None, description='营业外收入')
    non_operating_expense: float | None = Field(None, description='营业外支出')
    total_profit: float | None = Field(None, description='利润总额')
    income_tax_expense: float | None = Field(None, description='所得税费用')
    net_profit: float | None = Field(None, description='净利润')
    operating_cash_inflow: float | None = Field(None, description='经营活动现金流入')
    operating_cash_outflow: float | None = Field(None, description='经营活动现金流出')
    net_operating_cash_flow: float | None = Field(None, description='经营活动现金流量净额')
    investing_cash_inflow: float | None = Field(None, description='投资活动现金流入')
    investing_cash_outflow: float | None = Field(None, description='投资活动现金流出')
    net_investing_cash_flow: float | None = Field(None, description='投资活动现金流量净额')
    financing_cash_inflow: float | None = Field(None, description='筹资活动现金流入')
    financing_cash_outflow: float | None = Field(None, description='筹资活动现金流出')
    net_financing_cash_flow: float | None = Field(None, description='筹资活动现金流量净额')
    net_cash_flow: float | None = Field(None, description='现金及现金等价物净增加额')
    beginning_cash_balance: float | None = Field(None, description='期初现金及现金等价物余额')
    ending_cash_balance: float | None = Field(None, description='期末现金及现金等价物余额')
    remarks: str | None = Field(None, description='备注')


class GetFinancialDataDetail(FinancialDataSchemaBase):
    """财务数据详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='财务数据 ID')
    deleted: int = Field(description='是否已删除')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
    deleted_time: datetime | None = Field(None, description='删除时间')
