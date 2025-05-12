import pytest

from app.config import testing_config
from app.models import CourseModel, UsersModel, create_session, global_init


@pytest.fixture
def db_session():
    global_init(db_file=testing_config.DATABASE_PATH)
    db_session = create_session()
    yield db_session


def test_user_creation(db_session):
    test_user = UsersModel(
        name="test_user",
        description="test_description",
    )
    test_user.set_password(password="test_password")
    db_session.add(test_user)
    db_session.commit()
    user: UsersModel = (
        db_session.query(UsersModel).filter_by(name="test_user").first()
    )
    assert user.description == "test_description"
    assert user.check_password("test_password") is True


def test_course_creation(db_session):
    test_course = CourseModel(
        theme="test",
        desires_of_user="test",
        user_id=1,
        course={
            "test": "test",
        },
    )
    db_session.add(test_course)
    db_session.commit()
    course = db_session.query(CourseModel).filter_by(theme="test").first()
    assert course.desires_of_user == "test"
    assert course.user_id == 1
    assert course.course == {
        "test": "test",
    }
