from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, select
from waitress import serve

from database.models import Quote, Author, User, Tag, quote_tag_association
from fill_db import fill_db

app = Flask(__name__)
app.secret_key = b't7rqkng)a=$(n-ioae1y8=s%1u#d%5^d@hh20dsxg%^1z8sbve'
db = SQLAlchemy()
login_manager = LoginManager()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:29an99fr@192.168.1.242:5432/postgres"
app.debug = True
app.env = "development"
db.init_app(app)
login_manager.init_app(app)


def top_ten_tags():
    tags = db.session.query(Tag.name, func.count(Quote.id)) \
        .join(Tag.quotes) \
        .group_by(Tag.name) \
        .order_by(func.count(Quote.id).desc()) \
        .limit(10) \
        .all()
    return tags


def get_author(author_name):
    return db.session.query(Author)\
        .filter(Author.fullname == author_name)\
        .first()


def get_all_quotes():
    return db.select(Quote).order_by(Quote.id)


def get_all_authors():
    return db.session.query(Author).all()


def get_all_tags():
    return db.session.query(Tag).all()


def get_quotes_by_tag(tag_name):
    return db.select(Quote).join(Quote.tags).filter(Tag.name == tag_name)


def add_quote_db(author_name, quote_text, tags_list):
    this_author = db.session.query(Author).where(Author.fullname == author_name).first()
    this_quote = quote_text
    this_tags = list(db.session.scalars(select(Tag).where(Tag.name.in_(tags_list))))

    quote = Quote(author_id=this_author.id,
                  quote=this_quote,
                  tags=this_tags)
    db.session.add(quote)
    db.session.commit()


def add_author_db(fullname, born_date, born_location, description):
    author = Author(fullname=fullname,
                    born_date=born_date,
                    born_location=born_location,
                    description=description)
    db.session.add(author)
    db.session.commit()


def add_tag_db(tag_name):
    tag = Tag(name=tag_name)
    db.session.add(tag)
    db.session.commit()


def paginate_quotes(page_num, quotes):
    return db.paginate(quotes, page=page_num, per_page=10, max_per_page=10)


def del_all_records():
    db.session.execute(quote_tag_association.delete())
    db.session.execute(Quote.__table__.delete())
    db.session.execute(Author.__table__.delete())
    db.session.execute(Tag.__table__.delete())
    db.session.commit()


@app.route("/", strict_slashes=False)
def index():
    quotes = paginate_quotes(1, get_all_quotes())
    tags = top_ten_tags()
    return render_template('quotes.html', quotes=quotes, tags=tags)


@app.route("/page/<page_num>", strict_slashes=False)
def page(page_num):
    quotes = paginate_quotes(int(page_num), get_all_quotes())
    tags = top_ten_tags()
    return render_template('quotes.html', quotes=quotes, tags=tags)


@app.route("/tag/<tag_name>/page/<page_num>", strict_slashes=False)
def tag_page(tag_name, page_num):
    quotes = paginate_quotes(int(page_num), get_quotes_by_tag(tag_name))
    tags = top_ten_tags()
    return render_template('quotes.html', quotes=quotes, tags=tags, tag_name=tag_name)


@app.route("/author/<author_name>", strict_slashes=False)
def author_page(author_name):
    author_name = author_name.replace('-', ' ')
    author = get_author(author_name)
    return render_template('author.html', author=author)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if username and password and confirm_password and password == confirm_password:
            try:
                user = User(login=username, password=password)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect("/")  # register + login sucsess
            except SQLAlchemyError:
                return redirect("/register")  # name already exists
        return redirect("/")  # password != confirm_password


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id == user_id).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = db.session.query(User).filter(User.login == username).first()
        if user and user.password == password:
            print('login success')
            login_user(user)
            return redirect("/")
        else:
            print('password incorrect')
            return redirect("/login")


@app.route("/add_quote", methods=['GET', 'POST'])
@login_required
def add_quote():
    if request.method == 'GET':
        all_authors = get_all_authors()
        all_tags = get_all_tags()
        return render_template('add_quote.html', all_authors=all_authors, all_tags=all_tags)
    else:  # POST
        this_author = request.form.get('author')
        this_quote = request.form.get('description')
        this_tags = request.form.getlist('tags')
        add_quote_db(this_author, this_quote, this_tags)
        return redirect('/')


@app.route("/add_author", methods=['GET', 'POST'])
@login_required
def add_author():
    if request.method == 'GET':
        return render_template('add_author.html')
    else:  # POST
        this_fullname = request.form.get('fullname')
        this_born_date = request.form.get('born_date')
        this_born_location = request.form.get('born_location')
        this_description = request.form.get('description')
        add_author_db(this_fullname, this_born_date, this_born_location, this_description)
        return redirect('/')


@app.route("/add_tag", methods=['GET', 'POST'])
@login_required
def add_tag():
    if request.method == 'GET':
        return render_template('add_tag.html')
    else:  # POST
        this_tag_name = request.form.get('tag_name')
        add_tag_db(this_tag_name)
        return redirect('/')


@app.route("/delete_quotes")
@login_required
def del_all_quotes():
    del_all_records()
    return redirect('/')


@app.route("/import_quotes")
@login_required
def import_all_quotes():
    fill_db()
    return redirect('/')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=80)
