from datetime import datetime
from pathlib import Path
from sqlalchemy import DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SceneRecord(Base):
    __tablename__ = "scenes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    segment_number: Mapped[int] = mapped_column(Integer, index=True)
    script: Mapped[str] = mapped_column(Text)
    image_prompt: Mapped[str] = mapped_column(Text)
    video_prompt: Mapped[str] = mapped_column(Text)


class JobRecord(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    segment_number: Mapped[int] = mapped_column(Integer, index=True)
    mode: Mapped[str] = mapped_column(String(10))
    provider: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(20), default="pending")


class ProviderRecord(Base):
    __tablename__ = "providers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    kind: Mapped[str] = mapped_column(String(30))


class OutputRecord(Base):
    __tablename__ = "outputs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    segment_number: Mapped[int] = mapped_column(Integer)
    mode: Mapped[str] = mapped_column(String(10))
    path: Mapped[str] = mapped_column(String(500))


class RetryRecord(Base):
    __tablename__ = "retries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    segment_number: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(Text)


class LogRecord(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(Text)


class ContinuityRecord(Base):
    __tablename__ = "continuity"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(100), unique=True)
    value: Mapped[str] = mapped_column(Text)


class SettingRecord(Base):
    __tablename__ = "settings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(100), unique=True)
    value: Mapped[str] = mapped_column(Text)


class Database:
    def __init__(self, path: Path) -> None:
        self.engine = create_engine(f"sqlite:///{path}", future=True)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)

    def init(self) -> None:
        Base.metadata.create_all(self.engine)
