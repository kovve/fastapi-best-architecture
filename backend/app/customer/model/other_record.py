import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class OtherRecord(Base):
    """其他记录表"""

    __tablename__ = 'cust_other_record'
    __table_args__ = ({'comment': '其他记录表'},)

    id: Mapped[id_key] = mapped_column(init=False)
    enterprise_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='关联企业ID')
    title: Mapped[str] = mapped_column(sa.String(128), comment='标题')
    record_type: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='记录类型')
    content: Mapped[str | None] = mapped_column(sa.Text, default=None, comment='内容')
    record_date: Mapped[str | None] = mapped_column(sa.String(16), default=None, comment='日期')
    file_path: Mapped[str | None] = mapped_column(sa.String(255), default=None, comment='附件路径')
