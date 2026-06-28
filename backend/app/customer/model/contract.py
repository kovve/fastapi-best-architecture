import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Contract(Base):
    """合同存档表"""

    __tablename__ = 'cust_contract'
    __table_args__ = (
        sa.UniqueConstraint('contract_no', 'deleted', name='uk_cust_contract_no_deleted'),
        {'comment': '合同存档表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    enterprise_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='关联企业ID')
    contract_no: Mapped[str] = mapped_column(sa.String(64), comment='合同编号')
    contract_name: Mapped[str] = mapped_column(sa.String(128), comment='合同名称')
    contract_type: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='合同类型')
    sign_date: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='签订日期')
    start_date: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='开始日期')
    end_date: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='结束日期')
    amount: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='合同金额')
    our_party: Mapped[str | None] = mapped_column(sa.String(128), default=None, comment='我方签约主体')
    counter_party: Mapped[str | None] = mapped_column(sa.String(128), default=None, comment='对方签约主体')
    status: Mapped[int] = mapped_column(default=1, comment='状态(0停用 1正常)')
    file_path: Mapped[str | None] = mapped_column(sa.String(255), default=None, comment='合同文件路径')
    remarks: Mapped[str | None] = mapped_column(sa.Text, default=None, comment='备注')
