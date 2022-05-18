from sqlalchemy.orm import Session

from schemas.database_schema import Role


class RoleRepository:

    @classmethod
    def get_all_roles(cls, session: Session):
        roles = session.query(Role).all()
        session.close()
        return roles

    @classmethod
    def get_role_by_id(cls, role_id: str, session: Session):
        role = session.query(Role).filter_by(role_id=role_id).first()
        session.close()
        return role

    @classmethod
    def get_role_by_name(cls, role_name: str, session: Session):
        role = session.query(Role).filter_by(role_name=role_name).first()
        session.close()
        return role

    @classmethod
    def add_new_role(cls, role: Role, session: Session):
        session.add(role)
        session.commit()
        session.close()