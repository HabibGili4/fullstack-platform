from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.user_model import User  # noqa: E402, F401
from app.models.post_model import Post  # noqa: E402, F401
from app.models.task_model import Task  # noqa: E402, F401
from app.models.product_model import Product  # noqa: E402, F401
from app.models.refresh_token_model import RefreshToken  # noqa: E402, F401
from app.models.account_model import Account  # noqa: E402, F401
