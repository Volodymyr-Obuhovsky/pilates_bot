from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, BigInteger, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Descriptions(Base):
    __tablename__ = "description"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    header: Mapped[str] = mapped_column(String(150), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=True)


class Banners(Base):
    __tablename__ = "banner"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(15), unique=True)
    image: Mapped[str] = mapped_column(String(150), nullable=True)
    description_id: Mapped[int] = mapped_column(ForeignKey("description.id", ondelete="SET NULL"), nullable=False)

    description: Mapped["Descriptions"] = relationship("Descriptions", backref="banner")


class Marathons(Base):
    __tablename__ = 'marathon'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=True, unique=True)
    price: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    image: Mapped[str] = mapped_column(String(150))
    discount: Mapped[int] = mapped_column(BigInteger, nullable=True)
    client_rate: Mapped[int] = mapped_column(Integer, default=0)
    rate: Mapped[int] = mapped_column(Integer, default=0)
    description_id: Mapped[int] = mapped_column(ForeignKey("description.id", ondelete="SET NULL"), nullable=False)

    description: Mapped["Descriptions"] = relationship("Descriptions", backref="marathon")


class Users(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=True)
    marathon_id: Mapped[int] = mapped_column(ForeignKey("marathon.id", ondelete="SET NULL"), nullable=False)

    marathon: Mapped["Marathons"] = relationship("Marathons", backref='user')
