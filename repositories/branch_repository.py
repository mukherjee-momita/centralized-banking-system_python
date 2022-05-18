from sqlalchemy.orm import Session

from schemas.database_schema import Branch


class BranchRepository:

    @classmethod
    def insert_new_branch_record(cls, branch: Branch, session: Session):
        session.add(branch)
        session.commit()
        session.close()

    @classmethod
    def find_branch_by_branch_name_and_bank_id(cls, branch_name: str, bank_id: str, session: Session):
        branch = session.query(Branch).filter_by(branch_name=branch_name, bank_id=bank_id).first()
        session.close()
        return branch

    @classmethod
    def find_branch_by_id(cls, branch_id: str, session: Session):
        branch = session.query(Branch).filter_by(branch_id=branch_id).first()
        session.close()
        return branch

    @classmethod
    def find_branch_by_email(cls, branch_email: str, session: Session):
        branch = session.query(Branch).filter_by(branch_email=branch_email).first()
        session.close()
        return branch

    @classmethod
    def find_branch_by_contact(cls, branch_contact: str, session: Session):
        branch = session.query(Branch).filter_by(branch_contact=branch_contact).first()
        session.close()
        return branch

    @classmethod
    def find_branch_by_bank_id(cls, b_id: str, session: Session):
        branches = session.query(Branch).filter_by(bank_id=b_id).all()
        session.close()
        return branches