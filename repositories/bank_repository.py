from sqlalchemy.orm import Session

from schemas.database_schema import Bank


class BankRepository:

    @classmethod
    def insert_new_bank_record(cls, bank: Bank, session: Session):
        session.add(bank)
        session.commit()
        session.close()

    @classmethod
    def find_bank_by_name(cls, b_name: str, session: Session):
        bank = session.query(Bank).filter_by(bank_name=b_name).first()
        session.close()
        return bank

    @classmethod
    def find_bank_by_email(cls, b_email: str, session: Session):
        bank = session.query(Bank).filter_by(bank_email=b_email).first()
        session.close()
        return bank

    @classmethod
    def find_bank_by_id(cls, b_id: str, session: Session):
        bank = session.query(Bank).filter_by(bank_id=b_id).first()
        session.close()
        return bank

    @classmethod
    def find_all_banks(cls, session: Session):
        banks = session.query(Bank).all()
        session.close()
        return banks