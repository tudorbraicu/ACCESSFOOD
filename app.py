from flask import *
from database import init_db, db_session
from models import *
from flask_login import LoginManager,login_required, current_user, login_user, logout_user

app = Flask(__name__)


auth = Blueprint('auth', __name__)

app.secret_key = "Change Me"

login_manager = LoginManager()
login_manager.login_view = 'login_get'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# home page
@app.route("/")
@login_required
def get_home():
    return render_template("home.html")

# login page
@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

# logout gets you back to login
@app.route('/logout', methods=['GET'])
@login_required
def logout_get():
    logout_user()
    return render_template('login.html')

# make sure that you can only log in with valid username and password
@app.route('/login', methods=['POST'])
def login_post():
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

# order food, delete the ordered options
@app.route("/orderfood", methods=['GET'])
@login_required
def get_food():
    foods = db_session.query(Food, Restaurant).filter(Food.rst_id == Restaurant.id).filter(Food.user_id == None).all()
    foods2 = db_session.query(Food, Restaurant, User).filter(Food.rst_id == Restaurant.id).filter(Food.user_id == User.id).all()

    return render_template("orderfood.html", foods = foods, foods2=foods2)

# post the different options
@app.route("/orderfood", methods=['POST'])
@login_required
def order_food():
   # login code goes here
    items = request.form.items()
    for item in items:
        foodid = int(item[1])
        food=db_session.query(Food).filter(Food.id == foodid).one()
        food.user_id = current_user.id
        db_session.commit()
    return redirect(url_for('order_food'))

# choose your restaurant and add food
@app.route("/addfood", methods=['GET', 'POST'])
@login_required
def add_food():
    # choose restaurant
    if request.method == "GET":
        restaurants = db_session.query(Restaurant)
        return render_template("addfood.html", rsts = restaurants)
    # add the foodname
    elif request.method == "POST":
        food_name = request.form["food_name"]
        rst_id = request.form["rst_id"]
        new_food = Food(food_name, rst_id)
        db_session.add(new_food)
        db_session.commit()
    return redirect(url_for("add_food"))

# hardcode some necessary data into the system
def populate_db():
    db_session.query(Restaurant).delete()
    db_session.commit()
    rst = Restaurant("The Melt", "2456 One street")
    db_session.add(rst)
    rst = Restaurant("Spaces", "1234 Second street")
    db_session.add(rst)
    rst = Restaurant("Arnold", "123 Stanford Drive")
    db_session.add(rst)
    rst = Restaurant("Dutch Goose", "2 Alejandra Avenue")
    db_session.add(rst)
    db_session.commit()

    db_session.query(User).delete()
    db_session.commit()
    usr = User("tudor", "1234", "c")
    db_session.add(usr)
    usr = User("noah", "1234", "a")
    db_session.add(usr)
    db_session.commit()

    db_session.query(Food).delete()
    db_session.commit()


if __name__ == "__main__":
    init_db()
    #this intializes the database and fills data in the database
    populate_db()
    app.run(port=8000, debug=True)
