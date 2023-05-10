from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "Change Me"

# TODO: Fill in methods and routes


@app.route("/")
def get_home():
    return render_template("home.html")


@app.route("/restaurant")
def get_rst():
    restaurants = db_session.query(Restaurant)
    return render_template("restaurant.html", rsts = restaurants)

@app.route("/food")
def get_food():
    foods = db_session.query(Food)
    return render_template("food.html", foods = foods)

@app.route("/add-food", methods=['GET', 'POST'])
def add_food():
    if request.method == "GET":
        restaurants = db_session.query(Restaurant)
        return render_template("newfood.html", rsts = restaurants)
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
