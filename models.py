import datetime
import os
from sqlalchemy import create_engine, Integer, String, func, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from atexit import register



POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "123")
POSTGRES_DB = os.getenv("POSTGRES_DB", "netology")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Advertisement(Base):
    __tablename__ = "app_advertisement"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    head: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner: Mapped[str] = mapped_column(String(32), nullable=False)

    @property
    def json(self):
        return {
            'id': self.id,
            'head': self.head,
            'create_time': self.create_time.isoformat(),
            'owner': self.owner
        }


Base.metadata.create_all(bind=engine)
register(engine.dispose)
