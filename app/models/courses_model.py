import sqlalchemy

from app.models.db_session import SqlAlchemyBase
from app.models.users_model import UsersModel


class CourseModel(SqlAlchemyBase):
    """Модель курса, в ней хранится курс."""

    __tablename__ = "courses"

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
    )
    theme = sqlalchemy.Column(
        sqlalchemy.String,
        nullable=False,
    )
    desires_of_user = sqlalchemy.Column(
        sqlalchemy.Text,
        nullable=True,
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(
            UsersModel.id,
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    local_model = sqlalchemy.Column(
        sqlalchemy.Boolean,
        nullable=False,
    )
    course = sqlalchemy.Column(
        sqlalchemy.JSON,
        nullable=False,
    )
    is_favorite = sqlalchemy.Column(
        sqlalchemy.BOOLEAN,
        default=False,
        nullable=False,
    )

    user = sqlalchemy.orm.relationship(
        UsersModel,
        back_populates="courses",
    )


UsersModel.courses = sqlalchemy.orm.relationship(
    CourseModel, order_by=CourseModel.id, back_populates="user"
)
