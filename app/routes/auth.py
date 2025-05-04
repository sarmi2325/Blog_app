#import required modules
from flask import Blueprint,render_template,request,redirect,url_for,flash
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,current_user,login_required
from app.model import User
from app import db

#create auth blueprint
auth=Blueprint('auth',__name__)


@auth.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        email = request.form['email']
        password=request.form['password']

        existing_user=User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return redirect(url_for('auth.register'))

        new_user=User(username=username,email=email,password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('admin/register.html')


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        user=User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            #flash('Login successful')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('admin/login.html')

@auth.route('/logout')
def logout():
    logout_user()
    #flash('Logged out successfully')
    return redirect(url_for('auth.login'))