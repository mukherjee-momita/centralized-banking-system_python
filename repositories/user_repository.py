from sqlalchemy.orm import Session

from schemas.database_schema import User


class UserRepository:

    @classmethod
    def find_all_users(cls, session: Session):
        users = session.query(User).all()
        session.close()
        return users

    @classmethod
    def find_user_by_email(cls, email: str, session: Session):
        user = session.query(User).filter_by(user_email=email).first()
        session.close()
        return user

    @classmethod
    def find_user_by_contact(cls, contact: str, session: Session):
        user = session.query(User).filter_by(user_contact=contact).first()
        session.close()
        return user

    @classmethod
    def find_user_by_id(cls, u_id: str, session: Session):
        user = session.query(User).filter_by(user_id=u_id).first()
        session.close()
        return user

    @classmethod
    def insert_new_user(cls, user: User, session: Session):
        session.add(user)
        session.commit()
        session.close()