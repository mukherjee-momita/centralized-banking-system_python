from flask import Flask

from routes.user_route import user_sign_up, user_sign_in, user_home, user_sign_out, show_all_users, add_or_view_token
from routes.admin_route import add_or_view_country, add_or_view_state, add_or_view_city, add_or_view_bank, add_or_view_branch

from utilities.database_utility import DatabaseUtility
from utilities.environment_utility import EnvironmentUtility

# create flask app
app = Flask(__name__, template_folder="templates")

# include user routes
app.add_url_rule(rule="/", view_func=user_home, methods=["GET"])
app.add_url_rule(rule="/home", view_func=user_home, methods=["GET"])
app.add_url_rule(rule="/register", view_func=user_sign_up, methods=["GET", "POST"])
app.add_url_rule(rule="/login", view_func=user_sign_in, methods=["GET", "POST"])
app.add_url_rule(rule="/logout", view_func=user_sign_out, methods=["GET"])
app.add_url_rule(rule="/user/token", view_func=add_or_view_token, methods=["GET", "POST"])

# include admin routes
app.add_url_rule(rule="/admin/users", view_func=show_all_users, methods=["GET"])
app.add_url_rule(rule="/admin/countries", view_func=add_or_view_country, methods=["GET", "POST"])
app.add_url_rule(rule="/admin/states", view_func=add_or_view_state, methods=["GET", "POST"])
app.add_url_rule(rule="/admin/city", view_func=add_or_view_city, methods=["GET", "POST"])
app.add_url_rule(rule="/admin/bank", view_func=add_or_view_bank, methods=["GET", "POST"])
app.add_url_rule(rule="/admin/branch", view_func=add_or_view_branch, methods=["GET", "POST"])

# initiate utilities
DatabaseUtility.initialize_database_utility()
EnvironmentUtility.initialize_environment_utility()

# set secret key
app.secret_key = EnvironmentUtility.get_environment_variable_value("app_secret_key")

# run flask app
if __name__ == "__main__":
    app.run(debug=True)
