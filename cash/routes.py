from flask import render_template, flash, redirect, url_for, request
from cash import app
from cash.forms import RegisterForm, LoginForm
from cash.model import Worker, Attendance, Left, Item, Calculator, Transactions
from cash import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/workspace', methods=['GET', 'POST'])
@login_required
def work_space():
    if request.method == 'POST':
        item = request.form.get('item')
        qty = request.form.get('qty')
        mark = Item.query.filter_by(barcode=item).first()
        # if item or qty is None:
        #     flash('This form must be filled', category='danger')
        if mark:
            milk = mark.price * int(qty)
            calculator_to = Calculator(Item_name=mark.name,
                                       item_price=mark.price,
                                       item_quantity=qty,
                                       item_total=milk,
                                       )
            db.session.add(calculator_to)
            db.session.commit()
        else:
            flash('This item does not exist', category='danger')
    maddd = Calculator.query.all()
    count = 0
    for i in maddd:
        count = count + i.item_total
    total = f'N{count}'
    madd = Calculator.query.all()

    return render_template('work_space.html', total=total, items=madd)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    mad = Calculator.query.get_or_404(id)
    db.session.delete(mad)
    db.session.commit()
    return redirect(url_for('work_space'))

@app.route("/delete_all")
@login_required
def delete_all():
    mad = Calculator.query.all()
    engine = []
    total_sum = 0
    for i in mad:
        engine.append([i.id, i.Item_name, i.item_price, i.item_quantity, i.item_total])
        total_sum = total_sum + i.item_total
        db.session.delete(i)
    transactions = Transactions(transactions_all=str(engine),
                                worker=current_user.employee_number,
                                transactions_total=total_sum)
    db.session.add(transactions)
    db.session.commit()
    return redirect(url_for('work_space'))

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Worker(first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                email_address=form.email_address.data,
                                employee_number=form.employee_number.data,
                                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Account created successfully! Welcome to Godman Markets {user_to_create.first_name}',
              category='success')

        return redirect(url_for('login_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'there was an error creating this profile: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_worker = Worker.query.filter_by(employee_number=form.employee_number.data).first()
        if attempted_worker and attempted_worker.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_worker)
            attendance = Attendance(employee_number=form.employee_number.data)
            db.session.add(attendance)
            db.session.commit()
            flash(f'Welcome to Work {current_user.first_name}', category='success')
            return redirect(url_for('work_space'))
        else:
            flash(f'EMP or password is not correct! please try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    worker_out = Left(worker=current_user.employee_number)
    db.session.add(worker_out)
    db.session.commit()
    flash(f'BYE', category='success')
    logout_user()
    flash("You have been logged out", category='success')
    return redirect(url_for('home_page'))


@app.route('/manager')
@login_required
def manager_page():
    worky = Item.query.all()
    return render_template('manager.html', worky=worky)