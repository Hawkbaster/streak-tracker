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
        steps=data["steps"],
        last_date=data["last_date"]
    )

@app.route("/checkin", methods=["POST"])
def checkin():
    today = str(date.today())
    data = db.get_data()

    streak = data["streak"]
    steps = data["steps"]
    last_date = data["last_date"]

    # 🔥 ВСЕГДА +1 шаг
    steps += 1

    # 🧠 проверяем streak только если это новый день
    if last_date != today:

        if last_date:
            last = date.fromisoformat(last_date)

            if (date.today() - last).days == 1:
                streak += 1
            else:
                streak = 1
        else:
            streak = 1

        # обновляем дату только если новый день
        last_date = today

    db.update_data(streak, steps, last_date)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)