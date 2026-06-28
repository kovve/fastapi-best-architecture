import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class FinancialData(Base):
    """客户财务数据表（资产负债表 + 利润表 + 现金流量表）"""

    __tablename__ = 'cust_financial_data'
    __table_args__ = (
        sa.UniqueConstraint('enterprise_id', 'year', 'deleted', name='uk_cust_financial_enterprise_year_deleted'),
        {'comment': '客户财务数据表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    enterprise_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='关联企业ID')
    year: Mapped[int] = mapped_column(sa.Integer, comment='财务年度')
    audit_status: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='审计状态(已审计/未审计)')

    # ==================== 资产负债表 ====================
    # 流动资产
    monetary_funds: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='货币资金')
    accounts_receivable: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='应收账款')
    prepayments: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='预付账款')
    other_receivables: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='其他应收款')
    inventory: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='存货')
    current_assets_total: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='流动资产合计')

    # 非流动资产
    fixed_assets_original: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='固定资产原值')
    accumulated_depreciation: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='累计折旧')
    fixed_assets_net: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='固定资产净值')
    construction_in_progress: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='在建工程')
    intangible_assets: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='无形资产')
    non_current_assets_total: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='非流动资产合计')

    # 资产总计
    total_assets: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='资产总计')

    # 流动负债
    short_term_borrowings: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='短期借款')
    accounts_payable: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='应付账款')
    advance_receipts: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='预收账款')
    employee_payables: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='应付职工薪酬')
    taxes_payable: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='应交税费')
    other_payables: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='其他应付款')
    current_liabilities_total: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='流动负债合计')

    # 非流动负债
    long_term_borrowings: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='长期借款')
    long_term_payables: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='长期应付款')
    non_current_liabilities_total: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='非流动负债合计')

    # 负债合计
    total_liabilities: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='负债合计')

    # 所有者权益
    paid_in_capital: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='实收资本')
    capital_reserve: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='资本公积')
    surplus_reserve: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='盈余公积')
    undistributed_profit: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='未分配利润')
    owners_equity_total: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='所有者权益合计')

    # ==================== 利润表 ====================
    revenue: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='营业收入')
    cost_of_sales: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='营业成本')
    sales_tax_surcharge: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='税金及附加')
    selling_expenses: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='销售费用')
    administrative_expenses: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='管理费用')
    financial_expenses: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='财务费用')
    operating_profit: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='营业利润')
    non_operating_income: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='营业外收入')
    non_operating_expense: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='营业外支出')
    total_profit: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='利润总额')
    income_tax_expense: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='所得税费用')
    net_profit: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='净利润')

    # ==================== 现金流量表 ====================
    operating_cash_inflow: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='经营活动现金流入')
    operating_cash_outflow: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='经营活动现金流出')
    net_operating_cash_flow: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='经营活动现金流量净额')
    investing_cash_inflow: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='投资活动现金流入')
    investing_cash_outflow: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='投资活动现金流出')
    net_investing_cash_flow: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='投资活动现金流量净额')
    financing_cash_inflow: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='筹资活动现金流入')
    financing_cash_outflow: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='筹资活动现金流出')
    net_financing_cash_flow: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='筹资活动现金流量净额')
    net_cash_flow: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='现金及现金等价物净增加额')
    beginning_cash_balance: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='期初现金及现金等价物余额')
    ending_cash_balance: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='期末现金及现金等价物余额')

    remarks: Mapped[str | None] = mapped_column(sa.Text, default=None, comment='备注')
