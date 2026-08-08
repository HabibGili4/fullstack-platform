from sqlalchemy.orm import Session

from app.models.account_model import Account


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, account_id: int) -> Account | None:
        return self.db.query(Account).filter(Account.id == account_id).first()

    def get_by_id_for_update(self, account_id: int) -> Account | None:
        return (
            self.db.query(Account)
            .filter(Account.id == account_id)
            .with_for_update()
            .first()
        )

    def update_balance(self, account: Account, new_balance: float) -> Account:
        account.balance = new_balance
        self.db.commit()
        self.db.refresh(account)
        return account
