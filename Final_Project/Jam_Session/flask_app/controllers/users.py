from flask import render_template, redirect, request, session, flash
from flask_app.models.instrument import Instrument
from flask_app.models.user import User
from flask_app import app

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/register')
def register():
    return render_template("login.html")

@app.route('/signup', methods=["POST"])
def create_user():
    if not User.validate_register(request.form):
        return redirect('/register')
    data ={
        "username": request.form['username'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form["password"])
    }
    id = User.register(data)
    session['user_id'] = id

    return redirect('/home')

@app.route('/login',methods=['POST'])
def login():
    
    user = User.login(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/register')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/register')
    session['user_id'] = user.id
    return redirect('/home')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_one({'id' : session['user_id']})
    return render_template('home.html', user = user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/update/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "id":id
    }
    return render_template("edit_profile.html",user=User.get_one(data))

@app.route('/update/user/<int:id>', methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
        'id' : id,
        'username' : request.form['username'],
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'state' : request.form['state'],
        'zip_code' : request.form['zip_code'],
        'user_id' : session['user_id']
    }
    User.update(data)
    return redirect('/home')

@app.route('/guest')
def guest():
    return render_template('guest.html', user=User.get_all())

@app.route('/search')
def search():
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_all()
    return render_template("search.html", user = user )

@app.route('/view/<int:id>')
def view(id):
    data = {
        'id' : id
    }
    return render_template('view.html', user = User.get_one(data))

@app.route('/delete/<int:id>')
def delete(id):
    data ={
        'id': id
    }
    User.delete_user(data)
    return redirect('/logout')