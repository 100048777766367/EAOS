import bcrypt
from pydantic import BaseModel, EmailStr

from packages.identity.domain.models import User
from packages.identity.domain.ports import UserRepository


class RegisterUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class RegisterUserUseCase:
    """Use case đăng ký người dùng mới, đảm bảo mã hóa mật khẩu và chống trùng lặp."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, request: RegisterUserRequest) -> User:
        # Kiểm tra email đã tồn tại chưa
        existing_user = self.repository.find_by_email(request.email)
        if existing_user:
            raise ValueError(f"User with email {request.email} already exists")

        # Sinh muối (salt) và mã hóa mật khẩu trực tiếp bằng bcrypt chuẩn
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(request.password.encode("utf-8"), salt)
        hashed_pw = hashed_bytes.decode("utf-8")

        user = User(
            email=request.email,
            username=request.username.strip(),
            hashed_password=hashed_pw,
        )
        return self.repository.save(user)