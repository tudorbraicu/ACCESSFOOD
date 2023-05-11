from flask import *
from database import init_db, db_session
from models import *
from flask_login import LoginManager,login_required, current_user, login_user, logout_user

app = Flask(__name__)


auth = Blueprint('auth', __name__)

# TODO: Change the secret key
app.secret_key = "Change Me"

# TODO: Fill in methods and routes
login_manager = LoginManager()
login_manager.login_view = 'login_get'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@login_required
def get_home():
    return render_template("home.html")

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')


@app.route('/logout', methods=['GET'])
@login_required
def logout_get():
    logout_user()
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login_get')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('get_home'))

@app.route("/restaurant")
def get_rst():
    restaurants = db_session.query(Restaurant)
    return render_template("restaurant.html", rsts = restaurants)

@app.route("/orderfood", methods=['GET'])
@login_required
def get_food():
    #foods = db_session.query(Food)
    foods = db_session.query(Food, Restaurant).filter(Food.rst_id == Restaurant.id).all()
    return render_template("orderfood.html", foods = foods)

@app.route("/orderfood", methods=['POST'])
@login_required
def order_food():
   # login code goes here
    items = request.form.items()
    for item in items:
        foodid = item[0][1]
        food=db_session.query(Food).filter(Food.id == foodid).one()
        food.user_id = current_user.id
        print(food.user_id)
        db_session.commit()
    return redirect(url_for('order_food'))


@app.route("/addfood", methods=['GET', 'POST'])
@login_required
def add_food():
    if request.method == "GET":
        restaurants = db_session.query(Restaurant)
        return render_template("addfood.html", rsts = restaurants)
    elif request.method == "POST":
        food_name = request.form["food_name"]
        rst_id = request.form["rst_id"]
        new_food = Food(food_name, rst_id)
        db_session.add(new_food)
        db_session.commit()
    return redirect(url_for("add_food"))

def populate_db():
    db_session.query(Restaurant).delete()
    db_session.commit()
    rst = Restaurant("The Melt", "2456 One street")
    db_session.add(rst)
    rst = Restaurant("Spaces", "1234 Second street")
    db_session.add(rst)
    db_session.commit()

    db_session.query(User).delete()
    db_session.commit()
    usr = User("tudor", "1234")
    db_session.add(usr)
    usr = User("noah", "1234")
    db_session.add(usr)
    db_session.commit()

    db_session.query(Food).delete()
    db_session.commit()


if __name__ == "__main__":
    init_db()
    #populate_db()
    app.run(port=8000, debug=True)
