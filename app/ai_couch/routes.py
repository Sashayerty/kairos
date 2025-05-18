import json
import time
from http import HTTPStatus

from flask import Blueprint, redirect, render_template, request, send_file
from flask_login import current_user, login_required, login_user, logout_user
from rich import print, print_json
from rich.panel import Panel

from app.agents import check, edit_course, gen_course, gen_plan, gen_prompt
from app.ai_couch.functions import convert_course_to_html
from app.config import config
from app.models import CourseModel, UsersModel, create_session

ai_couch = Blueprint(
    "ai_couch",
    __name__,
    template_folder="../templates/ai_couch",
)
pretty_log = Panel


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
        use_beta=config.BETA_FUNCTIONS,
    )


@ai_couch.route(
    "/create-course",
    methods=[
        "POST",
        "GET",
    ],
)
def create_course():
    db_session = create_session()
    users_theme = request.form.get("users_theme")
    users_desires = request.form.get("users_desires")
    use_local_models = request.form.get("use_local_models") == "on"
    print(f" * Use local models: {use_local_models}")
    if not users_theme:
        return (
            render_template(
                "index.html",
                message="Тема курса не указана",
                title="Kairos - Главная",
                current_user=current_user,
                use_beta=config.BETA_FUNCTIONS,
            ),
            HTTPStatus.BAD_REQUEST,
        )
    print(f" * User's theme: {users_theme}")
    if users_desires:
        print(f" * User's desires: {users_desires}")
    if config.CENSOR_CHECK_ENABLED:
        answer_from_censor = json.loads(
            check(
                theme=users_theme,
                desires=users_desires,
                use_local_models=use_local_models,
            )
        )
        is_theme_are_good = answer_from_censor["data"]
    else:
        is_theme_are_good = True
    print(f" * User's theme and desires is good: {is_theme_are_good}")
    time.sleep(1.5)
    message = answer_from_censor["reason"] if not is_theme_are_good else None
    if message:
        print(message)
        return render_template(
            "index.html",
            message=message,
            title="Kairos - Главная",
            current_user=current_user,
            use_beta=config.BETA_FUNCTIONS,
        )
    else:
        prompt_from_llm = gen_prompt(
            theme=users_theme,
            desires=users_desires,
            description_of_user=(
                current_user.description
                if current_user.is_authenticated
                else None
            ),
            use_local_models=use_local_models,
        )
        print(
            pretty_log(
                prompt_from_llm,
                style="yellow",
                title="Промпт",
                title_align="left",
            )
        )
        time.sleep(1)
        plan_of_course: dict = json.loads(
            gen_plan(
                prompt=prompt_from_llm,
                use_local_models=use_local_models,
            )
        )
        print_json(data=plan_of_course)
        print("[green] * Plan of course created successfully![/green]")
        time.sleep(1)
        print(" * Course function invoked successfully!")
        course = convert_course_to_html(
            gen_course(
                prompt=prompt_from_llm,
                plan=plan_of_course,
                use_local_models=use_local_models,
            )
        )
        if course:
            print("[green] * Course created successfully![/green]")
        if current_user.is_authenticated:
            course_model = CourseModel(
                theme=users_theme,
                desires_of_user=users_desires,
                user_id=current_user.id,
                local_model=use_local_models,
                course=course,
            )
            db_session.add(course_model)
            db_session.commit()
        return render_template(
            "course.html",
            course=course_model,
            current_user=current_user,
            title="Kairos - Курс",
            use_beta=config.BETA_FUNCTIONS,
        )


@ai_couch.route(
    "/reg",
    methods=[
        "POST",
        "GET",
    ],
)
def register():
    db_session = create_session()
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        password_again = request.form.get("password_again")
        if (
            not name or not password or not password_again
        ):  # Если запросы через curl/postman
            return (
                render_template(
                    "register.html",
                    message="Все поля обязательны!",
                ),
                HTTPStatus.BAD_REQUEST,
            )
        if password != password_again:
            return (
                render_template(
                    "register.html",
                    message="Пароли не совпадают.",
                ),
                HTTPStatus.BAD_REQUEST,
            )
        if db_session.query(UsersModel).filter_by(name=name).first():
            return (
                render_template(
                    "register.html",
                    message="Пользователь с таким именем уже есть!",
                ),
                HTTPStatus.BAD_REQUEST,
            )
        if len(password) < 8 or len(password_again) < 8:
            return (
                render_template(
                    "register.html",
                    message="Длина пароля должна быть не менее 8 символов!",
                ),
                HTTPStatus.BAD_REQUEST,
            )
        user = UsersModel(
            name=name,
        )
        user.set_password(password=password)
        db_session.add(user)
        db_session.commit()
        return redirect("/login")
    return render_template(
        "register.html",
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
    db_session = create_session()
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        remember_me = request.form.get("remember_me", type=bool)
        user = db_session.query(UsersModel).filter_by(name=name).first()
        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            return redirect("/")
        else:
            return render_template(
                "login.html",
                message="Неправильный логин или пароль.",
            )
    return render_template(
        "login.html",
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
    db_session = create_session()
    if request.method == "POST":
        new_users_data = dict(request.form.items())
        if current_user.name != new_users_data["name"] and (
            db_session.query(UsersModel)
            .filter_by(name=new_users_data["name"])
            .first()
        ):
            return render_template(
                "profile.html",
                title="Kairos - Профиль",
                current_user=current_user,
                message="Данное имя занято!",
            )
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
    db_session = create_session()
    course = db_session.query(CourseModel).filter_by(id=course_id).first()
    return render_template(
        "course.html",
        title="Kairos - Курс",
        course=course,
        current_user=current_user,
    )


@ai_couch.route("/delete-course/<int:course_id>", methods=["POST", "GET"])
@login_required
def delete_course(course_id: int):
    db_session = create_session()
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
    db_session = create_session()
    course = db_session.query(CourseModel).filter_by(id=course_id).first()
    user_edits = request.form.get("user_edits")
    print(
        pretty_log(
            f" * Правки: {user_edits}",
            style="yellow",
            title="Правки",
            title_align="left",
        )
    )
    course.course = edit_course(
        course=course.course,
        user_edits=user_edits,
    )
    print_json(course.course)
    db_session.commit()
    return redirect(f"/course/{course_id}")


@ai_couch.route("/favorites/<int:course_id>", methods=["POST", "GET"])
@login_required
def favorites(course_id: int):
    db_session = create_session()
    course = db_session.query(CourseModel).filter_by(id=course_id).first()
    course.is_favorite = True if not course.is_favorite else False
    db_session.commit()
    return redirect("/courses")
