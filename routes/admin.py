from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.user import User
from models.assignment import Assignment


admin = Blueprint("admin", __name__)


@admin.route("/admin")
@login_required
def dashboard():

    if not current_user.is_admin:
        return "Access denied", 403

    users = User.query.all()
    assignments = Assignment.query.all()

    total_users = len(users)
    total_assignments = len(assignments)

    pending_assignments = len([
        assignment
        for assignment in assignments
        if assignment.status == "Pending"
    ])

    completed_assignments = len([
        assignment
        for assignment in assignments
        if assignment.status == "Completed"
    ])

    return render_template(
        "admin/dashboard.html",
        users=users,
        assignments=assignments,
        total_users=total_users,
        total_assignments=total_assignments,
        pending_assignments=pending_assignments,
        completed_assignments=completed_assignments
    )