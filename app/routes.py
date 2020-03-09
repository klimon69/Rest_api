# -*- coding: utf-8 -*-

from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import Users, Transactions
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, SendMoneyForm
import requests




@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    

    base_curr = current_user.currency
    if base_curr == 'BTC':
        curr_data = 'Путин: "Криптовалюты используют для мошенничества и терроризма." Вы не можете совершать операции с данной валютой.'
        
        return render_template("btc.html", curr_data=curr_data)

    form = SendMoneyForm()
    response = requests.get('https://api.exchangeratesapi.io/latest?base=' + base_curr)
    curr_data = response.json()

    #Забераем список валют EUR, USD, GPB, RUB, BTC
    
    curr_list = ['EUR', 'USD', 'GBP', 'RUB']
    if base_curr in curr_list: curr_list.remove(base_curr)
    dict_of_currs = { i : curr_data["rates"][i] for i in curr_list }
    

    if form.validate_on_submit():
        recipient = Users.query.filter_by(email=form.recipient.data).first()
        if recipient is None:
            flash('Получатель не найден')
            user_transactions = Transactions.query.filter_by(send_from=current_user.email).all()
            return redirect(url_for('index'))

        if int(form.amount.data) > int(current_user.reg_balance):
            flash('На вашем счёте недостаточно  средств')
            return redirect(url_for('index'))
        
        #Считаем конвертацию
        rate = curr_data["rates"][recipient.currency]
        amnt = form.amount.data

        send_to_recipient = (float(rate)*int(amnt))/1
        
        Users.query.filter_by(email=form.recipient.data).update({'reg_balance': int(recipient.reg_balance) + int(send_to_recipient)})
        db.session.commit()
        Users.query.filter_by(email=current_user.email).update({'reg_balance': int(current_user.reg_balance) - int(form.amount.data)})
        db.session.commit()
        transaction = Transactions(send_from=current_user.email,
        			 			   send_to=recipient.email,
        			 			   send_amount=form.amount.data)
        db.session.add(transaction)
        db.session.commit()

        #user_transactions = Transactions.filter_by(email=current_user.email).all()

        flash('Перевод успешно выполнен')
    user_transactions = Transactions.query.filter_by(send_from=current_user.email).all()
    form.recipient.data = ""
    form.amount.data = ""

    return render_template("index.html", title='', form=form, user_transactions=user_transactions, curr_data=dict_of_currs)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
#@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(reg_balance=form.reg_balance.data,
        			 currency= dict(form.currency.choices).get(form.currency.data),
        			 email=form.email.data)

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Теперь вы зарегестрированный пользователь!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


