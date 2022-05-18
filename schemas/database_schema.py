from sqlalchemy import Column, String, Boolean, ForeignKey

from utilities.database_utility import DatabaseUtility


# schema: role
class Role(DatabaseUtility.get_declarative_base()):
    __tablename__ = "roles"

    role_id = Column(type_=String(100), unique=True, nullable=False, index=True, primary_key=True)
    role_name = Column(type_=String(100), unique=True, nullable=False, index=True)


# schema: user
class User(DatabaseUtility.get_declarative_base()):
    __tablename__ = "users"

    user_id = Column(type_=String(100), unique=True, nullable=False, index=True, primary_key=True)
    user_first_name = Column(type_=String(100), nullable=False)
    user_middle_name = Column(type_=String(100))
    user_last_name = Column(type_=String(100), nullable=False)
    user_email = Column(type_=String(100), unique=True, nullable=False, index=True)
    user_contact = Column(type_=String(20), unique=True, nullable=False, index=True)
    user_enabled = Column(type_=Boolean, nullable=False, default=True)
    user_password = Column(type_=String(100), nullable=False)

    # relationships
    user_role = Column(ForeignKey("roles.role_id"), type_=String(100))


# schema: country
class Country(DatabaseUtility.get_declarative_base()):
    __tablename__ = "countries"

    country_id = Column(type_=String(100), unique=True, nullable=False, index=True, primary_key=True)
    country_name = Column(type_=String(100), unique=True, nullable=False, index=True)


# schema: state
class State(DatabaseUtility.get_declarative_base()):
    __tablename__ = "states"

    state_id = Column(type_=String(100), unique=True, nullable=False, index=True, primary_key=True)
    state_name = Column(type_=String(100), nullable=False)

    # relationship
    country_id = Column(ForeignKey("countries.country_id"), type_=String(100))


# schema: city_data
class City(DatabaseUtility.get_declarative_base()):
    __tablename__ = "cities"

    city_id = Column(type_=String(100), unique=True, nullable=False, index=True, primary_key=True)
    city_name = Column(type_=String(100), nullable=False)

    # relationship
    state_id = Column(ForeignKey("states.state_id"), type_=String(100))


# schema: address
class Address(DatabaseUtility.get_declarative_base()):
    __tablename__ = "addresses"

    address_id = Column(type_=String(100), unique=True, nullable=False, index=True, primary_key=True)
    address_building_no = Column(type_=String(100), nullable=False)
    address_line = Column(type_=String(100), nullable=False)
    address_zip_code = Column(type_=String(20), nullable=False)
    address_landmark = Column(type_=String(100))

    # relationship
    address_city = Column(ForeignKey("cities.city_id"), type_=String(100))


# schema: bank
class Bank(DatabaseUtility.get_declarative_base()):
    __tablename__ = "banks"

    bank_id = Column(type_=String(100), unique=True, nullable=False, index=True, primary_key=True)
    bank_name = Column(type_=String(100), unique=True, nullable=False, index=True)
    bank_email = Column(type_=String(100), unique=True, nullable=False, index=True)

    # relationship
    bank_address = Column(ForeignKey("addresses.address_id"), type_=String(100))


# schema: branch
class Branch(DatabaseUtility.get_declarative_base()):
    __tablename__ = "branches"

    branch_id = Column(type_=String(100), unique=True, nullable=False, index=True, primary_key=True)
    branch_name = Column(type_=String(100), nullable=False, index=True)
    branch_email = Column(type_=String(100), unique=True, nullable=False, index=True)
    branch_contact = Column(type_=String(100), unique=True, nullable=False, index=True)

    # relationship
    bank_id = Column(ForeignKey("banks.bank_id"), type_=String(100))
    branch_address = Column(ForeignKey("addresses.address_id"), type_=String(100))


# schema: token
class Token(DatabaseUtility.get_declarative_base()):
    __tablename__ = "tokens"

    token_id = Column(type_=String(100), unique=True, nullable=False, index=True, primary_key=True)
    token_created_on = Column(type_=String(100), nullable=False)
    token_date =  Column(type_=String(100), nullable=False)

    # relationship
    token_bank_id = Column(ForeignKey("banks.bank_id"), type_=String(100))
    token_branch_id = Column(ForeignKey("branches.branch_id"), type_=String(100))
    token_user_id = Column(ForeignKey("users.user_id"), type_=String(100))
