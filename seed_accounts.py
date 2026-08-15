from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models.account_model import Account

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()
try:
    # Cek apakah sudah ada data
    existing = db.query(Account).count()
    if existing > 0:
        print(f"Database sudah memiliki {existing} accounts. Skip seed.")
    else:
        account1 = Account(name="Habib", balance=100000)
        account2 = Account(name="Gillzz", balance=50000)
        db.add_all([account1, account2])
        db.commit()
        print("Seed data berhasil ditambahkan:")
        print(f"  Account 1: Habib  -> Rp {account1.balance:,.0f}")
        print(f"  Account 2: Gillzz -> Rp {account2.balance:,.0f}")
finally:
    db.close()
