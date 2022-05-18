from fpdf import FPDF
import datetime

from schemas.database_schema import Token
from services.user_service import get_user_by_id
from services.bank_service import get_bank_by_id
from services.branch_service import get_branch_by_branch_id
from services.address_service import get_address_by_id
from services.state_service import get_state_by_id
from services.country_service import get_country_by_id
from services.city_service import get_city_by_city_id

class TokenUtility:

    @classmethod
    def extract_token_pdf_data(cls, token: Token):
        user = get_user_by_id(token.token_user_id)
        user_name = user.user_first_name+" "
        if not user.user_middle_name is None:
            user_name += user.user_middle_name+" "
        user_name += user.user_last_name
        
        current_date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        booking_date_time = token.token_created_on

        bank = get_bank_by_id(token.token_bank_id)

        temp_address = get_address_by_id(bank.bank_address)
        bank_address = temp_address.address_building_no+", "+temp_address.address_line+", "
        bank_address += get_city_by_city_id(temp_address.address_city).city_name+", "
        bank_address += get_state_by_id(get_city_by_city_id(temp_address.address_city).state_id).state_name+", "
        bank_address += get_country_by_id(get_state_by_id(get_city_by_city_id(temp_address.address_city).state_id).country_id).country_name+", "
        bank_address += temp_address.address_zip_code+", Landmark: "+temp_address.address_landmark

        branch = get_branch_by_branch_id(token.token_branch_id)

        temp_address = get_address_by_id(branch.branch_address)
        branch_address = temp_address.address_building_no+", "+temp_address.address_line+", "
        branch_address += get_city_by_city_id(temp_address.address_city).city_name+", "
        branch_address += get_state_by_id(get_city_by_city_id(temp_address.address_city).state_id).state_name+", "
        branch_address += get_country_by_id(get_state_by_id(get_city_by_city_id(temp_address.address_city).state_id).country_id).country_name+", "
        branch_address += temp_address.address_zip_code+", Landmark: "+temp_address.address_landmark

        return cls.create_token_pdf(user_name=user_name,
                                    user_email=user.user_email,
                                    user_contact=user.user_contact,
                                    current_date_time=current_date_time,
                                    token_id=token.token_id,
                                    booking_date_time=booking_date_time,
                                    bank_name=bank.bank_name,
                                    bank_email=bank.bank_email,
                                    bank_address=bank_address,
                                    branch_name=branch.branch_name,
                                    branch_email=branch.branch_email,
                                    branch_contact=branch.branch_contact,
                                    branch_address=branch_address)

    @classmethod
    def create_token_pdf(cls, 
                         user_name: str,
                         user_email: str,
                         user_contact: str,
                         current_date_time: str,
                         token_id: str,
                         booking_date_time: str,
                         bank_name: str,
                         bank_email: str,
                         bank_address: str,
                         branch_name: str,
                         branch_contact: str,
                         branch_email: str,
                         branch_address: str):
        pdf_file = FPDF(orientation="P", format="A4", unit="mm")
        pdf_file.add_page()
        pdf_file.set_font(family="Arial", size=10)

        pdf_file.cell(200, 10, txt="Centralized Banking System", align="C", ln=1)

        pdf_file.cell(200, 10, txt=f"User: {user_name}", align="L", ln=3)
        pdf_file.cell(200, 10, txt=f"User Email: {user_email}", align="L", ln=4)
        pdf_file.cell(200, 10, txt=f"User Contact: {user_contact}", align="L", ln=5)
        pdf_file.cell(200, 10, txt=current_date_time, align="L", ln=6)

        pdf_file.cell(200, 10, txt=f"Token ID: {token_id}", align="L", ln=8)
        pdf_file.cell(200, 10, txt=f"Slot Time: {booking_date_time}", align="L", ln=9)

        pdf_file.cell(200, 10, txt=f"Bank Name: {bank_name}", align="L", ln=11)
        pdf_file.cell(200, 10, txt=f"Bank Email: {bank_email}", align="L", ln=12)
        pdf_file.cell(200, 10, txt=f"Bank Address: {bank_address}", align="L", ln=12)

        pdf_file.cell(200, 10, txt=f"Branch Name: {branch_name}", align="L", ln=16)
        pdf_file.cell(200, 10, txt=f"Branch Email: {branch_email}", align="L", ln=17)
        pdf_file.cell(200, 10, txt=f"Branch Contact: {branch_contact}", align="L", ln=18)
        pdf_file.cell(200, 10, txt=f"Branch Address: {branch_address}", align="L", ln=19)

        _file_name = f"{user_name}_token_{current_date_time}.pdf"

        pdf_file.output("output/token.pdf", "F")