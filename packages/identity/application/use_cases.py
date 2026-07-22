import bcrypt
from pydantic import BaseModel, EmailStr

from packages.identity.domain.models import User
from packages.identity.domain.ports import UserRepository


class RegisterUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str


class RegisterUserUseCase:
    """Use case Ä‘Äƒng kÃ½ ngÆ°á»i dÃ¹ng má»›i, Ä‘áº£m báº£o mÃ£ hÃ³a máº­t kháº©u vÃ  chá»‘ng trÃ¹ng láº·p."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, request: RegisterUserRequest) -> User:
        # Kiá»ƒm tra email Ä‘Ã£ tá»“n táº¡i chÆ°a
        existing_user = self.repository.find_by_email(request.email)
        if existing_user:
            raise ValueError(f"User with email {request.email} already exists")

        # Sinh muá»‘i (salt) vÃ  mÃ£ hÃ³a máº­t kháº©u trá»±c tiáº¿p báº±ng bcrypt chuáº©n
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(request.password.encode("utf-8"), salt)
        hashed_pw = hashed_bytes.decode("utf-8")

        user = User(
            email=request.email,
            username=request.username.strip(),
            hashed_password=hashed_pw,
        )
        return self.repository.save(user)

