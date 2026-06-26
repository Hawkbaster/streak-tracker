from flask import Flask, render_template, redirect, request, session  # импорт Flask и нужных функций
import db  # импорт нашей базы данных

app = Flask(__name__)  # создаём Flask приложение
app.secret_key = "secret-key-change-this"  # ключ для сессий (нужен чтобы хранить login)

db.init_db()  # создаём таблицы при запуске


@app.route("/")  # главная страница
def home():
    if "user_id" not in session:  # если пользователь НЕ залогинен
        return redirect("/login")  # отправляем на страницу логина

    data = db.get_data(session["user_id"])  # получаем данные текущего пользователя

    return render_template(
        "index.html",  # отдаём HTML страницу
        progress=data["progress"],  # передаём прогресс в шаблон
        total_steps=data["total_steps"]  # передаём шаги в шаблон
    )


@app.route("/step", methods=["POST"])  # кнопка +1 шаг
def step():
    user_id = session["user_id"]  # берём id пользователя из сессии

    data = db.get_data(user_id)  # получаем текущие данные

    progress = data["progress"] + 1  # увеличиваем прогресс
    total_steps = data["total_steps"] + 1  # увеличиваем общий счётчик

    if progress > 100:  # если дошли до конца сетки
        progress = 1  # начинаем заново

    db.update_data(user_id, progress, total_steps)  # сохраняем в базу

    return redirect("/")  # возвращаемся на главную


@app.route("/reset", methods=["POST"])  # кнопка сброса
def reset():
    user_id = session["user_id"]  # берём пользователя

    data = db.get_data(user_id)  # получаем данные

    db.update_data(user_id, 0, data["total_steps"])  # сбрасываем прогресс, но не шаги

    return redirect("/")  # возвращаемся на главную


# ---------- РЕГИСТРАЦИЯ ----------

@app.route("/register", methods=["GET", "POST"])  # страница регистрации
def register():
    if request.method == "POST":  # если отправили форму
        username = request.form["username"]  # берём username из формы
        password = request.form["password"]  # берём password из формы

        user_id = db.create_user(username, password)  # создаём пользователя
        session["user_id"] = user_id  # сохраняем логин (входим автоматически)

        return redirect("/")  # отправляем на главную

    return render_template("register.html")  # показываем форму


@app.route("/login", methods=["GET", "POST"])  # страница входа
def login():
    if request.method == "POST":  # если отправили форму
        username = request.form["username"]  # берём username
        password = request.form["password"]  # берём password

        user = db.get_user(username)  # ищем пользователя

        if user and user[2] == password:  # если пользователь есть и пароль совпадает
            session["user_id"] = user[0]  # сохраняем login
            return redirect("/")  # идём на главную

        return "Wrong login"  # ошибка если не совпало

    return render_template("login.html")  # показываем форму


@app.route("/logout")  # выход из аккаунта
def logout():
    session.clear()  # очищаем сессию (разлогин)
    return redirect("/login")  # отправляем на логин


if __name__ == "__main__":  # запуск приложения
    app.run(debug=True)  # включаем режим разработки