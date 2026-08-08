from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import get_current_user
from app.schemas.account import AccountResponse, TransferRequest, TransferResponse
from app.services.account_service import AccountService

router = APIRouter(prefix="/api/v1/accounts", tags=["Accounts"])


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    service = AccountService(db)
    return service.get_by_id(account_id)


@router.post("/transfer", response_model=TransferResponse)
def transfer(body: TransferRequest, db: Session = Depends(get_db)):
    service = AccountService(db)
    result = service.transfer(
        from_id=body.from_account_id,
        to_id=body.to_account_id,
        amount=body.amount,
    )
    return {
        "message": "transfer berhasil",
        "from_account": result["from_account"],
        "to_account": result["to_account"],
    }
