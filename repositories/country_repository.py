from sqlalchemy.orm import Session

from schemas.database_schema import Country


class CountryRepository:

    @classmethod
    def insert_new_country(cls, country: Country, session: Session):
        session.add(country)
        session.commit()
        session.close()

    @classmethod
    def find_country_by_id(cls, c_id: str, session: Session):
        country = session.query(Country).filter_by(country_id=c_id).first()
        session.close()
        return country

    @classmethod
    def find_country_by_name(cls, c_name: str, session: Session):
        country = session.query(Country).filter_by(country_name=c_name).first()
        session.close()
        return country

    @classmethod
    def find_all_countries(cls, session: Session):
        countries = session.query(Country).all()
        session.close()
        return countries