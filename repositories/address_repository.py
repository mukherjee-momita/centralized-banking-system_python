from sqlalchemy.orm import Session

from schemas.database_schema import Address


class AddressRepository:

    @classmethod
    def insert_new_address_record(cls, address: Address, session: Session):
        session.add(address)
        session.commit()
        session.close()

    @classmethod
    def find_address_by_id(cls, a_id: str, session: Session):
        address = session.query(Address).filter_by(address_id=a_id).first()
        session.close()
        return address