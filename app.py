from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


#Connect and create database
connect_db(app)
db.create_all()

#Add app to debug tool
toolbar = DebugToolbarExtension(app)


#--------------------------------------------------------------------------#
#                           Start Routes 
#--------------------------------------------------------------------------#

@app.route('/')
def home_page():
    """ Home route """
    return redirect('/register')


#--------------------------------------------------------------------------#
#                   Register, Login, and Logout Routes
#--------------------------------------------------------------------------#

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Register User: Validate submissions, create a new user, add user to session """
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Sorry, but this username is taken.  Please pick another')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Welcome! Your Account has been created!', "success")
        return redirect(f'/users/{new_user.username}')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Login a user if they provide a valid username and password else have them try again"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    """Logout user by removing their username from the session"""
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')


#--------------------------------------------------------------------------#
#                   User Access Routes (Only available if logged in)
#--------------------------------------------------------------------------#

@app.route('/users/<username>')
def show_user(username):
    """For logged in user, show their profile information"""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    user = User.query.get_or_404(username) 
    if user.username == session['username']:
        fb = Feedback.query.filter_by(username=user.username)
        return render_template('users.html', user=user,feedback=fb)
    flash("You don't have permission to see this account!", "danger")
    return redirect('/')


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """If logged user, chooses to delete their account all data will be removed from user and feedback table"""
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/')
    user = User.query.get_or_404(username) 
    if user.username == session['username']:
        session.pop('username')
        db.session.delete(user)
        db.session.commit()
        flash("Your account has been deleted!", "info")
        return redirect('/')
    flash("You don't have permission to delete this account!", "danger")
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """User can add feedback which will be saved to feedback table"""
    form = FeedbackForm()
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    u = User.query.filter_by(username=username).first()
    if u.username != session['username']:
        flash("You don't have permission to add feedback on this account!", "danger")
        return redirect('/')
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        fb = Feedback(title=title, content=content, username=u.username)
        db.session.add(fb)
        db.session.commit()
        flash("Feedback added", "success")
        return redirect(f'/users/{u.username}')
    return render_template('add.html', form=form)


@app.route('/feedback/<int:id>/update', methods=["GET", "POST"])
def update_feedback(id):
    """Update feedback only for user logged in"""
    fb = Feedback.query.get(id)
    if 'username' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    if fb.username != session['username']:
        flash("You don't have permission to update feedback on this account!", "danger")
        return redirect('/')
    form = FeedbackForm(obj=fb)
    if form.validate_on_submit():
        fb.title = form.title.data
        fb.content = form.content.data
        db.session.commit()
        return redirect(f"/users/{fb.username}")
    return render_template("update.html", form=form, feedback=fb)



@app.route('/feedback/<int:id>/delete', methods=["POST"])
def delete_feedback(id):
    """Delete feedback only for user logged in"""
    if 'username' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')
    fb = Feedback.query.get_or_404(id)
    if fb.username == session['username']:
        db.session.delete(fb)
        db.session.commit()
        flash("Feedback deleted!", "info")
        username = session['username']
        return redirect(f'/users/{username}')
    flash("You don't have permission to delete this item!", "danger")
    return redirect('/')

