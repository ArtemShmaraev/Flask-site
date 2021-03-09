from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.add_job import AddJobForm
from data.login_form import LoginForm
from data.users import User
from data.jobs import Jobs
from data.register import RegisterForm
from data.deljob import DelJobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)


def main():
    app.run(port=8000, host='127.0.0.1')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("index.html", jobs=jobs, names=names, title='Список вакансий')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Это пользователь уже существует")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            position=form.position.data,
            email=form.email.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    if current_user.is_authenticated:
        add_form = AddJobForm()
        if add_form.validate_on_submit():
            print(1)
            db_sess = db_session.create_session()
            jobs = Jobs(
                job=add_form.job.data,
                team_leader=current_user.id,
                work_size=add_form.work_size.data,
                collaborators=add_form.collaborators.data,
                is_finished=add_form.is_finished.data
            )
            db_sess.add(jobs)
            db_sess.commit()
            return redirect('/')
        return render_template('addjob.html', title='Добавить вакансию', form=add_form)
    return redirect('/')


@app.route('/editjob/<id>', methods=['GET', 'POST'])
def editjob(id):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if current_user.id == jobs.team_leader or current_user.id == 1:
            add_form = AddJobForm()
            if add_form.validate_on_submit():
                jobs.job = add_form.job.data
                jobs.team_leader = current_user.id
                jobs.work_size = add_form.work_size.data
                jobs.collaborators = add_form.collaborators.data
                jobs.is_finished = add_form.is_finished.data
                db_sess.commit()
                return redirect('/')
            return render_template('addjob.html', title='Редактировать вакансию', form=add_form)
        return redirect('/')
    return redirect('/')


@app.route('/deljob/<id>', methods=['GET', 'POST'])
def deljob(id):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        if current_user.id == jobs.team_leader or current_user.id == 1:
            add_form = DelJobForm()
            if add_form.validate_on_submit():
                f = add_form.is_finished.data
                if f:
                    db_sess.delete(jobs)
                    db_sess.commit()
                    return redirect('/')
                else:
                    return redirect('/')
            return render_template('deljob.html', title='Удалить вакансию', form=add_form)
        return redirect('/')
    return redirect('/')


if __name__ == '__main__':
    db_session.global_init("db/mars.db")
    main()
