from pydantic import BaseModel, Field


class AccountResponse(BaseModel):
    id: int
    name: str
    balance: float


class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float = Field(gt=0)


class TransferResponse(BaseModel):
    message: str
    from_account: AccountResponse
    to_account: AccountResponse
