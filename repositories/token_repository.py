from sqlalchemy.orm import Session

from schemas.database_schema import Token


class TokenRepository:

    @classmethod
    def find_token_by_id(cls, t_id: str, session: Session):
        token = session.query(Token).filter_by(token_id=t_id).first()
        session.close()
        return token

    @classmethod
    def insert_new_token_record(cls, token: Token, session: Session):
        session.add(token)
        session.commit()
        session.close()

    @classmethod
    def find_token_by_user_id(cls, u_id: str, session: Session):
        tokens = session.query(Token).filter_by(token_user_id=u_id).all()
        session.close()
        return tokens