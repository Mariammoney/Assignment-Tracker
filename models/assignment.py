
from datetime import date

from extensions import db


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    course = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=True)

    due_date = db.Column(db.Date, nullable=False)

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("Users.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="assignments"
    )

    @property
    def deadline_status(self):
        if self.status and self.status.lower() == "completed":
            return "Completed"

        if self.due_date < date.today():
            return "Overdue"

        if self.due_date == date.today():
            return "Due Today"

        return "Upcoming"

    def __repr__(self):
        return f"<Assignment {self.title}>"
