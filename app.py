from flask import Flask, render_template, redirect
import db

app = Flask(__name__)

db.init_db()


@app.route("/")
def home():
    data = db.get_data()

    return render_template(
        "index.html",
        progress=data["progress"],
        total_steps=data["total_steps"]
    )


@app.route("/step", methods=["POST"])
def step():
    data = db.get_data()

    progress = data["progress"] + 1
    total_steps = data["total_steps"] + 1

    if progress > 100:
        progress = 1

    db.update_data(progress, total_steps)

    return redirect("/")


@app.route("/reset", methods=["POST"])
def reset():
    data = db.get_data()

    db.update_data(
        0,
        data["total_steps"]
    )

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)