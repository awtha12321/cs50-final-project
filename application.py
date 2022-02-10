from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import random
import time
from flask_mail import Mail, Message
from html import unescape
from helper import login_required, apology, check, anime, search_anime_name, search_manga_name, anime_genre, manga, manga_genre, anime_name, manga_name

app = Flask(__name__)
mail = Mail(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mynameisayt12321@gmail.com'
app.config['MAIL_PASSWORD'] = 'can\'t tell you'
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQL("sqlite:///accounts.db")

genres = [
    "action",
    "adventure",
    "comedy",
    "drama",
    "ecchi",
    "fantasy",
    "horror",
    "mahou shoujo",
    "mecha",
    "music",
    "mystery",
    "psychological",
    "romance",
    "sci-fi",
    "slice of life",
    "sports",
    "supernatural",
    "thriller"
]

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    return redirect("/animes")

@app.route("/contact_us", methods=["GET", "POST"])
@login_required
def contact():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name:
            return apology("missing name")
        if not email:
            return apology("missing email")
        if not message:
            return apology("missing message")

        if check(email) == False:
            return apology("Email is not correct!")

        msg = Message("AYT (webapp)", sender = 'senorita38461@gmail.com', recipients = [email])
        msg.body = "thank you for sending me an email"
        mail.send(msg)

        msg = Message(name, sender = 'senorita38461@gmail.com', recipients = ['awayatha12321@gmail.com'])
        msg.body = message
        mail.send(msg)

        sent = True

        return render_template("contact.html", sent=sent)
    else:
        return render_template("contact.html")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    name = session["name"]
    email = session["email"]
    return render_template("profile.html", name=name, email=email)

@app.route("/anime-info", methods=["GET", "POST"])
@login_required
def anime_info():

    if request.method == "POST":

        name = request.form.get("name")
        info = search_anime_name(name)

        name, char_img, role, age = ([] for t in range(4))

        Etitle = info["Etitle"]
        bannerImage = info["bannerImage"]
        coverImage = info["coverImage"]

        if info["description"] is not None:
            des = unescape(info["description"])
        else:
            des = None

        age = info["age"]
        rating = info["rating"]
        Rtitle = info["Rtitle"]
        genres = info["genres"]
        episode = info["episode"]
        duration = info["duration"]
        season = info["season"]
        popular = info["popular"]
        status = info["status"]
        average = info["average"]
        gender = info["gender"]
        summary = info["summary"]

        # print(bannerImage)

        for i in range(len(info["image"])):

            name_tmp = info["name"][i]

            if name_tmp not in name:

                char_img.append(info["image"][i])
                role.append(info["role"][i])
                name.append(info["name"][i])
                age.append(info["age"][i])

        infor = {
            "name": name,
            "age": age,
            "gender": gender,
            "char_img": char_img,
            "rating": rating,
            "role": role,
            "coverImage": coverImage,
            "bannerImage": bannerImage,
            "des": des,
            "genres": genres,
            "Etitle": Etitle,
            "Rtitle": Rtitle,
            "episode": episode,
            "duration": duration,
            "season": season,
            "popular": popular,
            "status": status,
            "average": average,
            "summary": summary
        }


        return render_template("anime-info.html", infor=infor)


@app.route("/searched_anime", methods=["GET", "POST"])
@login_required
def searched_anime():

    if request.method == "POST":

        name = request.form.get("name")
        result = anime_name(name)

        # print(genre)

        coverImage, Rtitle, Etitle = ([] for t in range(3))

        if result["total"] == 0:
            return render_template("animes.html", total=result["total"], name=name)

        if result["adult"] is not None:
            adult = result["adult"]

        for i in range(len(result["coverImage"])):
            if adult[i] == False:
                coverImage.append(result["coverImage"][i])
                Rtitle.append(result["Rtitle"][i])
                Etitle.append(result["Etitle"][i])

        info = {
            "coverImage": coverImage,
            "Rtitle": Rtitle,
            "Etitle": Etitle
        }

        return render_template("animes.html", info=info, genres=genres)

@app.route("/animes", methods=["GET", "POST"])
@login_required
def animes():

    if request.method == "POST":

        genre = request.form.get("genres")
        ran = random.randrange(60, 75)
        result = anime_genre(ran, genre)

        # print(genre)

        coverImage, Rtitle, Etitle = ([] for t in range(3))

        if result["adult"] is not None:
            adult = result["adult"]

        for i in range(len(result["coverImage"])):
            if adult[i] == False:
                coverImage.append(result["coverImage"][i])
                Rtitle.append(result["Rtitle"][i])
                Etitle.append(result["Etitle"][i])

        info = {
            "coverImage": coverImage,
            "Rtitle": Rtitle,
            "Etitle": Etitle
        }

        return render_template("animes.html", info=info, genres=genres)

    else:

        ran = random.randrange(65, 75)
        result = anime(ran)

        coverImage, Rtitle, Etitle = ([] for t in range(3))

        if result["adult"] is not None:
            adult = result["adult"]

        for i in range(len(result["coverImage"])):
            if adult[i] == False:
                coverImage.append(result["coverImage"][i])
                Rtitle.append(result["Rtitle"][i])
                Etitle.append(result["Etitle"][i])

        info = {
            "coverImage": coverImage,
            "Rtitle": Rtitle,
            "Etitle": Etitle
        }

        return render_template("animes.html", info=info, genres=genres)

@app.route("/manga-info", methods=["GET", "POST"])
@login_required
def manga_info():

    if request.method == "POST":

        name = request.form.get("name")
        info = search_manga_name(name)

        name, char_img, role, age = ([] for t in range(4))

        Etitle = info["Etitle"]
        bannerImage = info["bannerImage"]
        coverImage = info["coverImage"]

        if info["description"] is not None:
            des = unescape(info["description"])
        else:
            des = None

        age = info["age"]
        rating = info["rating"]
        Rtitle = info["Rtitle"]
        native = info["native"]
        genres = info["genres"]
        chapter = info["chapter"]
        volume = info["volume"]
        season = info["season"]
        popular = info["popular"]
        status = info["status"]
        average = info["average"]
        gender = info["gender"]
        summary = info["summary"]

        # print(bannerImage)
        # print(native)

        for i in range(len(info["image"])):

            name_tmp = info["name"][i]

            if name_tmp not in name:

                char_img.append(info["image"][i])
                role.append(info["role"][i])
                name.append(info["name"][i])
                age.append(info["age"][i])

        infor = {
            "name": name,
            "age": age,
            "gender": gender,
            "char_img": char_img,
            "rating": rating,
            "role": role,
            "coverImage": coverImage,
            "bannerImage": bannerImage,
            "des": des,
            "genres": genres,
            "Etitle": Etitle,
            "Rtitle": Rtitle,
            "chapter": chapter,
            "volume": volume,
            "season": season,
            "popular": popular,
            "status": status,
            "average": average,
            "summary": summary,
            "native": native
        }


        return render_template("manga-info.html", infor=infor)

@app.route("/searched_manga", methods=["GET", "POST"])
@login_required
def mangas_search():

    if request.method == "POST":

        name = request.form.get("name")
        result = manga_name(name)

        # print(genre)

        coverImage, Rtitle, Etitle = ([] for t in range(3))

        if result["total"] == 0:
            return render_template("mangas.html", total=result["total"], name=name)

        if result["adult"] is not None:
            adult = result["adult"]

        for i in range(len(result["coverImage"])):
            if adult[i] == False:
                coverImage.append(result["coverImage"][i])
                Rtitle.append(result["Rtitle"][i])
                Etitle.append(result["Etitle"][i])

        info = {
            "coverImage": coverImage,
            "Rtitle": Rtitle,
            "Etitle": Etitle
        }

        return render_template("mangas.html", info=info, genres=genres)

@app.route("/mangas", methods=["GET", "POST"])
@login_required
def mangas():

    if request.method == "POST":

        genre = request.form.get("genres")
        ran = random.randrange(60, 75)
        result = manga_genre(ran, genre)

        # print(genre)

        coverImage, Rtitle, Etitle = ([] for t in range(3))

        if result["adult"] is not None:
            adult = result["adult"]

        for i in range(len(result["coverImage"])):
            if adult[i] == False:
                coverImage.append(result["coverImage"][i])
                Rtitle.append(result["Rtitle"][i])
                Etitle.append(result["Etitle"][i])

        info = {
            "coverImage": coverImage,
            "Rtitle": Rtitle,
            "Etitle": Etitle
        }

        return render_template("mangas.html", info=info, genres=genres)

    else:

        ran = random.randrange(65, 75)
        result = manga(ran)

        coverImage, Rtitle, Etitle = ([] for t in range(3))

        if result["adult"] is not None:
            adult = result["adult"]

        for i in range(len(result["coverImage"])):
            if adult[i] == False:
                coverImage.append(result["coverImage"][i])
                Rtitle.append(result["Rtitle"][i])
                Etitle.append(result["Etitle"][i])

        info = {
            "coverImage": coverImage,
            "Rtitle": Rtitle,
            "Etitle": Etitle
        }

        return render_template("mangas.html", info=info, genres=genres)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("pass")

        if not email:
            return apology("Email is missing!")
        if not password:
            return apology("Password is missing!")

        row = db.execute("SELECT * FROM user WHERE email = ?", email)

        if len(row) != 1:
            return apology("User not found!")

        if len(row) != 1 or not check_password_hash(row[0]["password"], password):
             return apology("Incorrect password!")

        session["id"] = row[0]["id"]
        session["email"] = row[0]["email"]
        session["name"] = row[0]["name"]

        time.sleep(2)
        return redirect("/animes")

    else:
        return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():

    session.clear()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("pass")
        password1 = request.form.get("pass2")

        if not name:
            return apology("missing name!")
        if not email:
            return apology("missing email")
        if not password or not password1:
            return apology("missing password!")

        if check(email) == False:
            return apology("Email is not correct!")

        if password != password1:
            return apology("passwords must be the same!")

        row = db.execute("SELECT * FROM user WHERE email = ?", email)

        if len(row) == 1:
            return apology("Email is already used")

        h_password = generate_password_hash(password,  method='pbkdf2:sha256', salt_length=8)

        insert = "INSERT INTO user (name, email, password) VALUES (?, ?, ?)"
        db.execute(insert, name, email, h_password)

        time.sleep(2)
        return redirect("/animes")

    else:
        return render_template("register.html")
