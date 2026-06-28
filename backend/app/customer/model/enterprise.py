import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Enterprise(Base):
    """客户企业信息表"""

    __tablename__ = 'cust_enterprise'
    __table_args__ = (
        sa.UniqueConstraint('name', 'deleted', name='uk_cust_enterprise_name_deleted'),
        {'comment': '客户企业信息表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(128), comment='企业名称')
    short_name: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='简称')
    unified_social_credit_code: Mapped[str | None] = mapped_column(
        sa.String(18), default=None, comment='统一社会信用代码'
    )
    legal_representative: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='法定代表人')
    registered_address: Mapped[str | None] = mapped_column(sa.String(255), default=None, comment='注册地址')
    business_scope: Mapped[str | None] = mapped_column(sa.Text, default=None, comment='经营范围')
    registered_capital: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='注册资本')
    establishment_date: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='成立日期')
    industry: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='所属行业')
    enterprise_type: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='企业类型')
    contact_person: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='联系人')
    contact_phone: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='联系电话')
    contact_email: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='联系邮箱')
    status: Mapped[int] = mapped_column(default=1, comment='状态(0停用 1正常)')
    remarks: Mapped[str | None] = mapped_column(sa.Text, default=None, comment='备注')
