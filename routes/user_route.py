from lib2to3.pgen2 import token
from flask import request, render_template, make_response, redirect, url_for, flash
from http import HTTPStatus

from services.user_service import register_user, login_user, view_all_users
from services.bank_service import get_all_banks, get_bank_by_id
from services.branch_service import get_branches_by_bank_id, get_branch_by_branch_id
from services.token_service import add_new_token, get_tokens_by_user_id
from utilities.cookie_utility import add_cookie, is_user_signed_in, get_current_user_data
from utilities.token_utility import TokenUtility
from errors.application_error import ApplicationError

# route for user sign up
def user_sign_up():
    # check if user is already signed in
    if is_user_signed_in(request=request):
        return redirect(url_for("user_home"))

    # if request method is GET
    if request.method == "GET":
        return render_template("register.html")
    
    # if request method is POST
    elif request.method == "POST":

        # extract user data
        first_name = request.form.get("first-name")
        middle_name = None if request.form.get("middle-name")=="" else request.form.get("middle-name")
        last_name = request.form.get("last-name")
        email = request.form.get("email")
        contact = request.form.get("contact")
        password = request.form.get("password")

        # register user
        try:
            register_user(first_name=first_name, middle_name=middle_name, last_name=last_name,
                                email=email, contact=contact, password=password)
            return redirect(url_for("user_sign_in"))
        except ApplicationError as err:
            flash(err.error_message)
            return redirect(url_for("user_sign_up"))

# route for user sign in
def user_sign_in():
    # check if user is already signed in
    if is_user_signed_in(request=request):
        return redirect(url_for("user_home"))
    
    # if request method is GET
    if request.method == "GET":
        return render_template("login.html")

    # if request method is POST
    elif request.method == "POST":

        # extract user data
        email = request.form.get("email")
        password = request.form.get("password")
        
        # login user
        try:
            # login user and get auth token
            auth_token = login_user(email=email, password=password)

            # split auth token
            tokens = auth_token.split(".")
            # prepare response
            response = make_response(redirect(url_for("user_home")))
            # add auth token to cookie
            for i in range(len(tokens)):
                add_cookie(response=response, key=f"token_{i}", value=tokens[i])
            
            # return response
            return response
        except ApplicationError as err:
            flash(err.error_message)
            return redirect(url_for("user_sign_in"))

# route for user home
def user_home():
    # check if user is signed in
    if not is_user_signed_in(request=request):
        return redirect(url_for("user_sign_in"))

    # if request method is GET
    if request.method == "GET":
        return render_template("index.html", 
                                current_user=get_current_user_data(request=request))

# route for user logout
def user_sign_out():
    # check if user is signed in
    if not is_user_signed_in(request=request):
        return redirect(url_for("user_sign_in"))

    # delete cookies and redirect to login page
    response = make_response(redirect(url_for("user_sign_in")))
    for i in range(3):
        response.set_cookie(f"token_{i}", "", expires=0)
    return response

# function to view all users
def show_all_users():
    # check if user is signed in
    if not is_user_signed_in(request=request):
        return redirect(url_for("user_sign_in"))
    
    # get current user data
    current_user = get_current_user_data(request=request)

    # check if user is admin
    if not current_user["user_role"] == "ADMIN":
        return redirect(url_for("user_home"))
    
    
    if request.method == "GET":
        # fetch all users data
        users = view_all_users()
        return render_template("user.html", users=users, current_user=current_user)

# function to add or view token
def add_or_view_token():
    # check if user is signed in
    if not is_user_signed_in(request=request):
        return redirect(url_for("user_sign_in"))
    
    # get current user data
    current_user = get_current_user_data(request=request)

    # check if user is admin
    if not current_user["user_role"] == "USER":
        return redirect(url_for("user_home"))
    
    # get all banks
    banks = get_all_banks()
    
    if request.method == "GET":
        # get tokens
        tokens = get_tokens_by_user_id(current_user["user_id"])
        
        tokens_list = []
        for token in tokens:
            tokens_list.append({
                "token_id": token.token_id,
                "token_bank": get_bank_by_id(token.token_bank_id).bank_name,
                "token_branch": get_branch_by_branch_id(token.token_branch_id).branch_name,
                "token_created_on": token.token_created_on,
                "token_date": token.token_date.replace("T", " ")
            })

        # get all branches
        branches = []
        for bank in banks:
            temp_branches = get_branches_by_bank_id(bank.bank_id)
            for branch in temp_branches:
                branches.append({
                    "branch_id": branch.branch_id,
                    "branch_name": bank.bank_name+" - "+branch.branch_name
                })
        return render_template("token.html",
                                current_user=current_user,
                                banks=banks,
                                branches=branches,
                                tokens=tokens_list)

    elif request.method == "POST":
        bank_id = request.form.get("bank-name")
        branch_id = request.form.get("branch-name")
        token_date = request.form.get("date")
        try:
            temp_branch = get_branch_by_branch_id(branch_id)
            print(temp_branch.bank_id == bank_id)

            if not get_branch_by_branch_id(branch_id).bank_id == bank_id:
                raise ApplicationError(HTTPStatus.BAD_REQUEST, 
                                        "selected branch is not a part of selected bank")

            new_token = add_new_token(bank_id, branch_id, token_date, current_user["user_id"])
            TokenUtility.extract_token_pdf_data(new_token)
            return redirect(url_for("add_or_view_token"))

        except ApplicationError as err:
            flash(err.error_message)
            return redirect(url_for("add_or_view_token"))
