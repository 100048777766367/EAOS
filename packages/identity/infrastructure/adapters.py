from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from packages.identity.domain.models import User
from packages.identity.domain.ports import UserRepository


class Base(DeclarativeBase):
    pass


class PostgresUserModel(Base):
    __tablename__ = "identity_users"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class PostgresUserRepository(UserRepository):
    """Adapter kết nối PostgreSQL cho Domain Identity."""

    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def save(self, user: User) -> User:
        db_session = self.SessionLocal()
        import uuid

        user_id = user.id or str(uuid.uuid4())
        db_model = PostgresUserModel(
            id=user_id,
            email=user.email,
            username=user.username,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            created_at=user.created_at,
        )
        try:
            db_session.add(db_model)
            db_session.commit()
            return User(
                id=user_id,
                email=user.email,
                username=user.username,
                hashed_password=user.hashed_password,
                is_active=user.is_active,
                created_at=user.created_at,
            )
        finally:
            db_session.close()

    def find_by_id(self, user_id: str) -> User | None:
        db_session = self.SessionLocal()
        try:
            db_model = db_session.query(PostgresUserModel).filter(PostgresUserModel.id == user_id).first()
            if not db_model:
                return None
            return User(
                id=db_model.id,
                email=db_model.email,
                username=db_model.username,
                hashed_password=db_model.hashed_password,
                is_active=db_model.is_active,
                created_at=db_model.created_at,
            )
        finally:
            db_session.close()

    def find_by_email(self, email: str) -> User | None:
        db_session = self.SessionLocal()
        try:
            db_model = db_session.query(PostgresUserModel).filter(PostgresUserModel.email == email).first()
            if not db_model:
                return None
            return User(
                id=db_model.id,
                email=db_model.email,
                username=db_model.username,
                hashed_password=db_model.hashed_password,
                is_active=db_model.is_active,
                created_at=db_model.created_at,
            )
        finally:
            db_session.close()
