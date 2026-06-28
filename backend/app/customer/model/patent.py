import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Patent(Base):
    """专利信息表"""

    __tablename__ = 'cust_patent'
    __table_args__ = ({'comment': '专利信息表'},)

    id: Mapped[id_key] = mapped_column(init=False)
    enterprise_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='关联企业ID')
    patent_name: Mapped[str] = mapped_column(sa.String(255), comment='专利名称')
    patent_no: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='专利号')
    patent_type: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='类型(发明/实用新型/外观设计)')
    application_no: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='申请号')
    application_date: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='申请日期')
    publication_date: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='公开日期')
    authorization_date: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='授权日期')
    patentee: Mapped[str | None] = mapped_column(sa.String(128), default=None, comment='专利权人')
    inventor: Mapped[str | None] = mapped_column(sa.String(128), default=None, comment='发明人')
    legal_status: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='法律状态')
    remarks: Mapped[str | None] = mapped_column(sa.Text, default=None, comment='备注')
