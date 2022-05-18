from flask import request, render_template, redirect, url_for, flash
from http import HTTPStatus

from errors.application_error import ApplicationError
from utilities.cookie_utility import is_user_signed_in, get_current_user_data
from services.country_service import get_all_countries, add_new_country, get_country_by_id
from services.state_service import add_new_state, get_state_by_id, get_states_by_country_id, get_all_states
from services.city_service import add_new_city, get_cities_by_state_id, get_all_cities, get_city_by_city_id
from services.bank_service import get_all_banks, add_new_bank, get_bank_by_id
from services.address_service import get_address_by_id
from services.branch_service import add_new_branch, get_branches_by_bank_id

# function to add or view country
def add_or_view_country():
    # check if user is signed in
    if not is_user_signed_in(request=request):
        return redirect(url_for("user_sign_in"))
    
    # get current user data
    current_user = get_current_user_data(request=request)

    # check if user is admin
    if not current_user["user_role"] == "ADMIN":
        return redirect(url_for("user_home"))

    if request.method == "GET":
        countries = get_all_countries()
        return render_template("country.html", countries=countries, current_user=current_user)
    elif request.method=="POST":
        country_name = request.form.get("country-name")
        try:
            add_new_country(country_name=country_name)
            return redirect(url_for("add_or_view_country"))
        except ApplicationError as err:
            flash(err.error_message)
            return redirect(url_for("add_or_view_country"))

# function to add or view state
def add_or_view_state():
    # check if user is signed in
    if not is_user_signed_in(request=request):
        return redirect(url_for("user_sign_in"))
    
    # get current user data
    current_user = get_current_user_data(request=request)

    # check if user is admin
    if not current_user["user_role"] == "ADMIN":
        return redirect(url_for("user_home"))

    # get all countries
    countries = get_all_countries()

    if request.method == "GET":
        return render_template("state.html", current_user=current_user, countries=countries)

    elif request.method=="POST":
        country_id_1 = request.form.get("country-name-1")
        country_id_2 = request.form.get("country-name-2")
        state_name = request.form.get("state-name")

        if state_name is None:
            states = get_states_by_country_id(country_id=country_id_2)
            return render_template("state.html", 
                                states=states, 
                                countries=countries, 
                                current_user=current_user)
        else:
            try:
                add_new_state(state_name=state_name, country_id=country_id_1)
                states = get_states_by_country_id(country_id=country_id_1)
                return render_template("state.html", 
                                states=states, 
                                countries=countries, 
                                current_user=current_user)
            except ApplicationError as err:
                flash(err.error_message)
                return redirect(url_for("add_state"))

# function to add or view city
def add_or_view_city():
    # check if user is signed in
    if not is_user_signed_in(request=request):
        return redirect(url_for("user_sign_in"))
    
    # get current user data
    current_user = get_current_user_data(request=request)

    # check if user is admin
    if not current_user["user_role"] == "ADMIN":
        return redirect(url_for("user_home"))

    # get all countries
    countries = get_all_countries()

    # get all states
    states = get_all_states()

    # prepare state data
    for state in states:
        state.state_name = get_country_by_id(state.country_id).country_name+" - "+state.state_name

    if request.method == "GET":
        return render_template("city.html", 
                                countries=countries,
                                states=states,
                                current_user=current_user)
    
    elif request.method == "POST":
        country_id_1 = request.form.get("country-name-1")
        state_id_1 = request.form.get("state-name-1")

        city_name = request.form.get("city-name")

        country_id_2 = request.form.get("country-name-2")
        state_id_2 = request.form.get("state-name-2")
        
        if city_name is None:
            try:
                if not get_state_by_id(state_id_2).country_id == country_id_2:
                    raise ApplicationError(HTTPStatus.BAD_REQUEST, 
                    "selected state does not belong to the selected country")
                
                cities = get_cities_by_state_id(state_id=state_id_2)
                return render_template("city.html",
                                            countries=countries,
                                            states=states,
                                            cities=cities,
                                            current_user=current_user)
            except ApplicationError as err:
                flash(err.error_message)
                return redirect(url_for("add_or_view_city"))
        else:
            try:
                if not get_state_by_id(state_id_1).country_id == country_id_1:
                    raise ApplicationError(HTTPStatus.BAD_REQUEST, 
                    "selected state does not belong to the selected country")

                add_new_city(city_name=city_name, state_id=state_id_1)
                cities = get_cities_by_state_id(state_id_1)
                return render_template("city.html",
                                        countries=countries,
                                        states=states,
                                        cities=cities,
                                        current_user=current_user)
            except ApplicationError as err:
                flash(err.error_message)
                return redirect(url_for("add_or_view_city"))

# function to add or view banks
def add_or_view_bank():
    # check if user is signed in
    if not is_user_signed_in(request=request):
        return redirect(url_for("user_sign_in"))
    
    # get current user data
    current_user = get_current_user_data(request=request)

    # check if user is admin
    if not current_user["user_role"] == "ADMIN":
        return redirect(url_for("user_home"))

    # get all countries
    countries = get_all_countries()

    # get all states and prepare data
    states = get_all_states()
    for state in states:
        state.state_name = get_country_by_id(state.country_id).country_name+" - "+state.state_name

    # get all cities and prepare data
    cities = get_all_cities()
    for city in cities:
        city.city_name = get_state_by_id(city.state_id).state_name+" - "+city.city_name
    
    if request.method == "GET":
        banks = []
        for bank in get_all_banks():
            # prepare address
            bank_address = get_address_by_id(bank.bank_address)
            address = bank_address.address_building_no+", "+bank_address.address_line+", "
            address += get_city_by_city_id(bank_address.address_city).city_name+", "
            address += get_state_by_id(get_city_by_city_id(bank_address.address_city).state_id).state_name+", "
            address += get_country_by_id(get_state_by_id(get_city_by_city_id(bank_address.address_city).state_id).country_id).country_name+", "
            address += bank_address.address_zip_code+", Landmark: "+bank_address.address_landmark


            banks.append({
                "bank_id": bank.bank_id,
                "bank_name": bank.bank_name,
                "bank_email": bank.bank_email,
                "bank_address": address
            })
        return render_template("bank.html",
                                countries=countries,
                                states=states,
                                cities=cities,
                                banks = banks,
                                current_user=current_user)
    elif request.method == "POST":
        bank_name = request.form.get("bank-name")
        bank_email = request.form.get("bank-email")
        building_no = request.form.get("building-no")
        line = request.form.get("line")
        zip_code = request.form.get("zip-code")
        landmark = request.form.get("landmark")
        country_code = request.form.get("country-name")
        state_code = request.form.get("state-name")
        city_code = request.form.get("city-name")
        try:
            if not get_state_by_id(state_code).country_id == country_code:
                raise ApplicationError(HTTPStatus.BAD_REQUEST, 
                            "selected state does not belong to the selected country")
            
            if not get_city_by_city_id(city_code).state_id == state_code:
                raise ApplicationError(HTTPStatus.BAD_REQUEST,
                            "selected city does not belong to the selected state")
        
        
            add_new_bank(bank_name, bank_email, building_no, line, zip_code, landmark, city_code)
            return redirect(url_for("add_or_view_bank"))
        except ApplicationError as err:
            flash(err.error_message)
            return redirect(url_for("add_or_view_bank"))

# function to add or view branches
def add_or_view_branch():
    # check if user is signed in
    if not is_user_signed_in(request=request):
        return redirect(url_for("user_sign_in"))
    
    # get current user data
    current_user = get_current_user_data(request=request)

    # check if user is admin
    if not current_user["user_role"] == "ADMIN":
        return redirect(url_for("user_home"))

    # get all countries
    countries = get_all_countries()

    # get all states and prepare data
    states = get_all_states()
    for state in states:
        state.state_name = get_country_by_id(state.country_id).country_name+" - "+state.state_name

    # get all cities and prepare data
    cities = get_all_cities()
    for city in cities:
        city.city_name = get_state_by_id(city.state_id).state_name+" - "+city.city_name
    
    # get all banks
    banks = get_all_banks()

    if request.method == "GET":
        return render_template("branch.html", 
                                current_user=current_user,
                                countries=countries,
                                states=states,
                                cities=cities,
                                banks=banks)
    elif request.method == "POST":
        view_branch_bank_id = request.form.get("view-branch-bank-name")
        bank_id = request.form.get("bank-name")
        branch_name = request.form.get("branch-name")
        branch_email = request.form.get("branch-email")
        branch_contact = request.form.get("branch-contact")
        building_no = request.form.get("building-no")
        line = request.form.get("line")
        zip_code = request.form.get("zip-code")
        landmark = request.form.get("landmark")
        country_code = request.form.get("country-name")
        state_code = request.form.get("state-name")
        city_code = request.form.get("city-name")
        try:
            if not view_branch_bank_id is None:
                branches = []
                for branch in get_branches_by_bank_id(view_branch_bank_id):
                    # prepare address
                    branch_address = get_address_by_id(branch.branch_address)
                    address = branch_address.address_building_no+", "+branch_address.address_line+", "
                    address += get_city_by_city_id(branch_address.address_city).city_name+", "
                    address += get_state_by_id(get_city_by_city_id(branch_address.address_city).state_id).state_name+", "
                    address += get_country_by_id(get_state_by_id(get_city_by_city_id(branch_address.address_city).state_id).country_id).country_name+", "
                    address += branch_address.address_zip_code+", Landmark: "+branch_address.address_landmark


                    branches.append({
                        "branch_id": branch.branch_id,
                        "branch_name": branch.branch_name,
                        "branch_email": branch.branch_email,
                        "branch_contact": branch.branch_contact,
                        "bank_name": get_bank_by_id(view_branch_bank_id).bank_name,
                        "branch_address": address
                    })

                    return render_template("branch.html",
                                countries=countries,
                                states=states,
                                cities=cities,
                                banks = banks,
                                branches=branches,
                                current_user=current_user)

            if not get_state_by_id(state_code).country_id == country_code:
                raise ApplicationError(HTTPStatus.BAD_REQUEST, 
                            "selected state does not belong to the selected country")
            
            if not get_city_by_city_id(city_code).state_id == state_code:
                raise ApplicationError(HTTPStatus.BAD_REQUEST,
                            "selected city does not belong to the selected state")
        
        
            add_new_branch(bank_id=bank_id,
                            branch_name=branch_name,
                            branch_email=branch_email,
                            branch_contact=branch_contact,
                            building_no=building_no,
                            line=line,
                            landmark=landmark,
                            zip_code=zip_code,
                            city_id=city_code)
            return redirect(url_for("add_or_view_branch"))
        except ApplicationError as err:
            flash(err.error_message)
            return redirect(url_for("add_or_view_branch"))
