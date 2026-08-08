from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.account_model import Account
from app.repositories.account_repository import AccountRepository


class AccountService:
    def __init__(self, db: Session):
        self.repo = AccountRepository(db)
        self.db = db

    def get_by_id(self, account_id: int) -> Account:
        account = self.repo.get_by_id(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="account tidak ditemukan")
        return account

    def transfer(self, from_id: int, to_id: int, amount: float):
        if from_id == to_id:
            raise HTTPException(status_code=400, detail="tidak bisa transfer ke diri sendiri")

        # Lock kedua baris untuk mencegah race condition
        from_account = self.repo.get_by_id_for_update(from_id)
        if not from_account:
            raise HTTPException(status_code=404, detail="account pengirim tidak ditemukan")

        to_account = self.repo.get_by_id_for_update(to_id)
        if not to_account:
            raise HTTPException(status_code=404, detail="account penerima tidak ditemukan")

        if float(from_account.balance) < amount:
            raise HTTPException(status_code=400, detail="saldo tidak mencukupi")

        try:
            # Kurangi saldo pengirim
            from_account.balance = float(from_account.balance) - amount

            # Tambah saldo penerima
            to_account.balance = float(to_account.balance) + amount

            self.db.commit()
            self.db.refresh(from_account)
            self.db.refresh(to_account)
        except Exception:
            self.db.rollback()
            raise HTTPException(status_code=500, detail="transfer gagal")

        return {
            "from_account": from_account,
            "to_account": to_account,
        }
