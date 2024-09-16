from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
from secret_key import SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField(
        "Cafe Name", validators=[DataRequired()], render_kw={"placeholder": "MyCafe"}
    )
    location = StringField(
        "Cafe Location On Google Map",
        validators=[DataRequired(), URL()],
        render_kw={"placeholder": "Like: https://goo.gl/maps/uoi89324893kio%v"},
    )
    open_time = StringField(
        "Opening Time",
        validators=[DataRequired()],
        render_kw={"placeholder": "8:50AM"},
    )
    close_time = StringField(
        "Closing Time",
        validators=[DataRequired()],
        render_kw={"placeholder": "10:50PM"},
    )
    coffee_rating = SelectField(
        "Coffee Rating", choices=["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    )
    wifi_rating = SelectField(
        "WiFi Strength",
        choices=[
            "💪",
            "💪💪",
            "💪💪💪",
            "💪💪💪💪",
            "💪💪💪💪💪",
        ],
    )
    submit = SubmitField("Submit")


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def cafes():
    list_of_rows = []
    try:
        with open("cafe-data.csv", newline="", encoding="utf-8") as csv_file:
            csv_data = csv.reader(csv_file, delimiter=",")
            header = next(csv_data)  # skip the header row
            list_of_rows = [row for row in csv_data]
    except FileNotFoundError:
        # Inform the user or redirect them to error page
        return render_template(
            "error.html", message="No cafe data found. Please add some data."
        )
    except csv.Error:
        # Handle CSV-specific errors
        return render_template("error.html", message="Error processing cafe data file.")

    return render_template("cafes.html", cafes=list_of_rows)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                [
                    form.cafe.data,
                    form.location.data,
                    form.open_time.data,
                    form.close_time.data,
                    form.coffee_rating.data,
                    form.wifi_rating.data,
                ]
            )
        return redirect(url_for("cafes"))
    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)