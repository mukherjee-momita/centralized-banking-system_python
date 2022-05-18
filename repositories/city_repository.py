from sqlalchemy.orm import Session

from schemas.database_schema import City


class CityRepository:

    @classmethod
    def find_all_cities(cls, session: Session):
        cities = session.query(City).all()
        session.close()
        return cities

    @classmethod
    def insert_new_city(cls, city: City, session: Session):
        session.add(city)
        session.commit()
        session.close()

    @classmethod
    def find_city_by_id(cls, c_id: str, session: Session):
        city = session.query(City).filter_by(city_id=c_id).first()
        session.close()
        return city

    @classmethod
    def find_city_by_city_name_and_state_id(cls, c_name: str, s_id: str, session: Session):
        city = session.query(City).filter_by(city_name=c_name, state_id=s_id).first()
        session.close()
        return city

    @classmethod
    def find_cities_by_state_id(cls, s_id: str, session: Session):
        cities = session.query(City).filter_by(state_id=s_id).all()
        session.close()
        return cities