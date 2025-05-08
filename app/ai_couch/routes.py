import json
import time

import colorama
from flask import Blueprint, redirect, render_template, request, send_file
from flask_login import current_user, login_required, login_user, logout_user

from app.ai_core import censor, cool_prompt, edit_course, get_theory, plan
from app.config import config
from app.forms import LoginForm, RegistrationForm
from app.models import CourseModel, UsersModel, create_session, global_init

ai_couch = Blueprint(
    "ai_couch",
    __name__,
    template_folder="../templates/ai_couch",
)
colorama.init(autoreset=True)
global_init(config.DATABASE_PATH)
db_session = create_session()


@ai_couch.route(
    "/",
    methods=[
        "POST",
        "GET",
    ],
)
def index():
    return render_template(
        "index.html",
        title="Kairos - Главная",
        current_user=current_user,
    )


@ai_couch.route(
    "/create-course",
    methods=[
        "POST",
        "GET",
    ],
)
def create_course():
    users_theme = dict(request.form.items())["users_theme"]
    users_desires = dict(request.form.items())["users_desires"]
    print(f" * User's theme: {users_theme}")
    if users_desires:
        print(f" * User's desires: {users_desires}")
    answer_from_censor = json.loads(
        censor(theme_from_user=users_theme, desires=users_desires)
    )
    is_theme_are_good = answer_from_censor["data"]
    print(
        f" * User's theme and desires is good:"
        f" {colorama.Fore.GREEN if is_theme_are_good else colorama.Fore.RED}{is_theme_are_good}"
    )
    time.sleep(1.5)
    message = answer_from_censor["reason"] if not is_theme_are_good else None
    if message:
        print(message)
        return render_template(
            "index.html",
            message=message,
            title="Kairos - Главная",
            current_user=current_user,
        )
    else:
        prompt_from_llm = cool_prompt(
            users_theme=users_theme,
            desires=users_desires,
            description_of_user=(
                current_user.description
                if current_user.is_authenticated
                else None
            ),
        )
        print(prompt_from_llm)
        time.sleep(1)
        plan_of_course: dict = json.loads(
            plan(prompt_from_llm=prompt_from_llm)
        )
        print(colorama.Fore.GREEN + " * Plan of course created successfully!")
        print(plan_of_course)
        time.sleep(1)
        print(" * Course function invoked successfully!")
        course = get_theory(
            prompt_from_prompt_agent=prompt_from_llm,
            plan=plan_of_course,
        )
        if course:
            print(colorama.Fore.GREEN + " * Course created successfully!")
        if current_user.is_authenticated:
            course_model = CourseModel(
                theme=users_theme,
                desires_of_user=users_desires,
                user_id=current_user.id,
                course=json.loads(course),
            )
            db_session.add(course_model)
            db_session.commit()
        return render_template(
            "course.html",
            course=json.loads(course),
            current_user=current_user,
            title="Kairos - Курс",
        )


@ai_couch.route(
    "/reg",
    methods=[
        "POST",
        "GET",
    ],
)
def register():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        if (
            registration_form.password.data
            == registration_form.password_again.data
        ):
            if (
                db_session.query(UsersModel)
                .filter_by(name=registration_form.name.data)
                .first()
            ):
                return render_template(
                    "register.html",
                    message="Пользователь с таким именем уже есть!",
                    form=registration_form,
                )
            user = UsersModel(
                name=registration_form.name.data,
            )
            user.set_password(password=registration_form.password.data)
            db_session.add(user)
            db_session.commit()
            return redirect("/login")
        else:
            return render_template(
                "register.html",
                message="Пароли не совпадают.",
                form=registration_form,
            )
    return render_template(
        "register.html",
        form=registration_form,
        title="Kairos - Регистрация",
    )


@ai_couch.route(
    "/login",
    methods=[
        "POST",
        "GET",
    ],
)
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = (
            db_session.query(UsersModel)
            .filter_by(name=login_form.name.data)
            .first()
        )
        if user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            return redirect("/")
        else:
            return render_template(
                "login.html",
                form=login_form,
                message="Неправильный логин или пароль.",
            )
    return render_template(
        "login.html",
        form=login_form,
        title="Kairos - Вход",
    )


@ai_couch.route(
    "/logout",
    methods=[
        "POST",
        "GET",
    ],
)
@login_required
def logout():
    logout_user()
    return redirect("/")


@ai_couch.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    if request.method == "POST":
        new_users_data = dict(request.form.items())
        user = (
            db_session.query(UsersModel).filter_by(id=current_user.id).first()
        )
        data_successfully_changed = user.change_data(
            new_name=new_users_data["name"],
            new_description=new_users_data["description"],
            new_password=new_users_data["password"],
            confirm_new_password=new_users_data["confirm_password"],
        )
        if data_successfully_changed[0]:
            db_session.commit()
        return render_template(
            "profile.html",
            title="Kairos - Профиль",
            current_user=current_user,
            message=data_successfully_changed[1],
        )
    return render_template(
        "profile.html",
        title="Kairos - Профиль",
        current_user=current_user,
    )


@ai_couch.route("/courses", methods=["POST", "GET"])
@login_required
def courses():
    courses_of_current_user = current_user.courses
    return render_template(
        "courses.html",
        title="Kairos - Мои курсы",
        courses_of_current_user=courses_of_current_user,
    )


@ai_couch.route(
    "/course/<int:course_id>",
    methods=[
        "POST",
        "GET",
    ],
)
@login_required
def course(course_id: int):
    course = db_session.query(CourseModel).filter_by(id=course_id).first()
    return render_template(
        "course.html",
        title="Kairos - Курс",
        course=course.course,
        current_user=current_user,
    )


@ai_couch.route("/delete-course/<int:course_id>", methods=["POST", "GET"])
@login_required
def delete_course(course_id: int):
    course = db_session.query(CourseModel).filter_by(id=course_id).first()
    db_session.delete(course) if course else None
    db_session.commit()
    return redirect("/courses")


@ai_couch.route("/terms", methods=["GET"])
def terms_of_using_kairos():
    return send_file("./static/terms/terms_of_using.pdf")


@ai_couch.route(
    "/edit-course/<int:course_id>",
    methods=["POST", "GET"],
)
@login_required
def edit_course_view(course_id: int):
    course = db_session.query(CourseModel).filter_by(id=course_id).first()
    user_edits = request.args.get("user_edits", type=str)
    course.course = edit_course(
        course=course.course,
        user_edits=user_edits,
    )
    db_session.commit()
    return redirect(f"/course/{course_id}")


@ai_couch.route("/favorites/<int:course_id>", methods=["POST", "GET"])
@login_required
def favorites(course_id: int):
    course = db_session.query(CourseModel).filter_by(id=course_id).first()
    course.is_favorite = True if not course.is_favorite else False
    db_session.commit()
    return redirect("/courses")
