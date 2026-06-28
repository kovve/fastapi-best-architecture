import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class ProjectRecord(Base):
    """申报项目记录表"""

    __tablename__ = 'cust_project_record'
    __table_args__ = ({'comment': '申报项目记录表'},)

    id: Mapped[id_key] = mapped_column(init=False)
    enterprise_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='关联企业ID')
    project_name: Mapped[str] = mapped_column(sa.String(128), comment='项目名称')
    project_type: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='项目类型')
    declaration_date: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='申报日期')
    declaration_amount: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='申报金额')
    approved_amount: Mapped[float | None] = mapped_column(sa.Numeric(18, 2), default=None, comment='批准金额')
    status: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='状态(申报中/已批准/未批准/已结题)')
    declaration_department: Mapped[str | None] = mapped_column(sa.String(128), default=None, comment='申报部门/机构')
    remarks: Mapped[str | None] = mapped_column(sa.Text, default=None, comment='备注')
