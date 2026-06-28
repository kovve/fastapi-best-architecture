import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class ServiceFee(Base):
    """服务费收取表"""

    __tablename__ = 'cust_service_fee'
    __table_args__ = ({'comment': '服务费收取表'},)

    id: Mapped[id_key] = mapped_column(init=False)
    enterprise_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='关联企业ID')
    fee_type: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='费用类型')
    amount: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='金额')
    receivable_date: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='应收日期')
    received_date: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='实收日期')
    payment_status: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='收款状态(未收/部分/已收)')
    invoice_no: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='发票号')
    invoice_date: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='开票日期')
    remarks: Mapped[str | None] = mapped_column(sa.Text, default=None, comment='备注')
