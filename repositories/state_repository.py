from sqlalchemy.orm import Session

from schemas.database_schema import State


class StateRepository:

    @classmethod
    def find_all_states(cls, session: Session):
        states = session.query(State).all()
        session.close()
        return states

    @classmethod
    def find_state_by_country_id_and_state_name(cls, c_id: str, s_name: str, session: Session):
        state = session.query(State).filter_by(country_id=c_id, state_name=s_name).first()
        session.close()
        return state

    @classmethod
    def find_state_by_country_id_and_state_id(cls, c_id: str, s_id: str, session: Session):
        state = session.query(State).filter_by(country_id=c_id, state_id=s_id).first()
        session.close()
        return state

    @classmethod
    def find_state_by_id(cls, s_id: str, session: Session):
        state = session.query(State).filter_by(state_id=s_id).first()
        session.close()
        return state

    @classmethod
    def find_states_by_country_id(cls, c_id: str, session: Session):
        states = session.query(State).filter_by(country_id=c_id).all()
        session.close()
        return states

    @classmethod
    def insert_new_state_record(cls, state: State, session: Session):
        session.add(state)
        session.commit()
        session.close()