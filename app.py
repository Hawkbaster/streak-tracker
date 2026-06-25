from flask import Flask, render_template, request, redirect
from datetime import date
import db

app = Flask(__name__)

db.init_db()

@app.route("/")
def home():
    data = db.get_data()

    return render_template(
        "index.html",
        streak=data["streak"],
        last_date=data["last_date"]
    )

@app.route("/checkin", methods=["POST"])
def checkin():
    today = str(date.today())
    data = db.get_data()

    if data["last_date"] == today:
        return redirect("/")

    streak = data["streak"]
    last_date = data["last_date"]

    if last_date:
        last = date.fromisoformat(last_date)

        if (date.today() - last).days == 1:
            streak += 1
        else:
            streak = 1
    else:
        streak = 1

    db.update_data(streak, today)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)