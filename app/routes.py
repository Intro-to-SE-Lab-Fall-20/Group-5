from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/test')
def test():
    user = {'username' : 'User'}
    return render_template('test.html', title = 'Home', user = user)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('test'))
    return render_template('login.html', title='Sign In', form=form)
