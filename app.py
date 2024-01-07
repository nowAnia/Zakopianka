from datetime import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zakopianka.db'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


# ----------------------------------
# MODELS
# ----------------------------------


class CarDrives(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enter_time = db.Column(db.DateTime, unique=False, nullable=False)
    exit_time = db.Column(db.DateTime, unique=False)
    registration = db.Column(db.String(100), unique=False, nullable=False)
    tunnel_id = db.Column(db.Integer, db.ForeignKey('tunnels.id'), nullable=False, )

    def speed(self):
        if self.exit_time:
            return round(self.tunnel.length / ((self.exit_time - self.enter_time).total_seconds() / 3600))
        return None


class Tunnels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    length = db.Column(db.Integer, unique=False, nullable=False)
    speed = db.Column(db.Integer, unique=False, nullable=False)
    car_drives = db.relationship('CarDrives', backref='tunnel', lazy='dynamic')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'length': self.length
        }


# ----------------------------------
# ROUTES
# ----------------------------------


@app.route('/enter_car_drives', methods=["POST"])
def enter_car_drives():
    car_licence = request.form.get("licence")
    if car_licence is None:
        return "licence parameter is required", 400

    tunnel_id = request.form.get("tunnel_id")
    if tunnel_id is None:
        return "tunnel_id parameter is required", 400

    enter_datetime_text = request.form.get("enter_datetime")
    if enter_datetime_text is None:
        return "enter_datetime parameter is required", 400

    try:
        enter_datetime = datetime.strptime(enter_datetime_text, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return f"Provided date {enter_datetime_text} is not in expected format: %Y-%m-%d %H:%M:%S", 400

    new_row = CarDrives(registration=car_licence, enter_time=enter_datetime, tunnel_id=tunnel_id)
    db.session.add(new_row)
    db.session.commit()
    return "Ok"



@app.route('/exit_car_drives', methods=["PUT"])
def exit_car_drives():
    car_licence = request.form.get("licence")
    if car_licence is None:
        return "licence parameter is required", 400
    exit_datetime_text = request.form.get("exit_datetime")
    if exit_datetime_text is None:
        return "exit_datetime parameter is required", 400

    try:
        exit_datetime = datetime.strptime(exit_datetime_text, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return f"Provided date {exit_datetime_text} is not in expected format: %Y-%m-%d %H:%M:%S", 400

    x = CarDrives.query.filter_by(registration=car_licence, exit_time=None).order_by(desc(CarDrives.enter_time)).first_or_404(
        description="No registration found.")
    x.exit_time = exit_datetime
    db.session.commit()
    return "Ok"


@app.route('/tunnels/<int:id>', methods=["GET"])
def dashboard(id):
    tunnel = Tunnels.query.filter_by(id=id).first_or_404(description="There is no tunnel with this id")
    y = tunnel.car_drives.all()

    return render_template('tunnel_view.html', car_drives=y, tunnel=tunnel)


@app.route('/tunnels', methods=["GET"])
def tunnels():
    t = Tunnels.query.all()

    if request.headers.get("Accept") == "application/json":
        t_jsons = [x.to_json() for x in t]
        return t_jsons
    else:
        return render_template('tunnels.html', tunnels=t)


# ----------------------------------
# RUN SERVER
# ----------------------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)
