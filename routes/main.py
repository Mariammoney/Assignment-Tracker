
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from extensions import db
from models.assignment import Assignment
from forms import AssignmentForm


main = Blueprint("main", __name__)


# Public landing page
@main.route("/")
def landing():
    return render_template("index.html")


# User dashboard
@main.route("/dashboard")
@login_required
def homepage():

    assignments = Assignment.query.filter_by(
        user_id=current_user.id
    ).all()

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
        "main/homepage.html",
        user=current_user,
        assignments=assignments,
        total_assignments=total_assignments,
        pending_assignments=pending_assignments,
        completed_assignments=completed_assignments
    )


# Add assignment
@main.route("/add-assignment", methods=["GET", "POST"])
@login_required
def add_assignment():

    form = AssignmentForm()

    if form.validate_on_submit():

        assignment = Assignment(
            title=form.title.data,
            course=form.course.data,
            description=form.description.data,
            due_date=form.due_date.data,
            status=form.status.data,
            user_id=current_user.id
        )

        db.session.add(assignment)
        db.session.commit()

        flash("Assignment added successfully.", "success")

        return redirect(url_for("main.homepage"))

    return render_template(
        "main/add_assignment.html",
        form=form
    )


# View assignment details



@main.route("/assignment/<int:assignment_id>")
@login_required
def assignment_detail(assignment_id):

    assignment = Assignment.query.filter_by(
        id=assignment_id,
        user_id=current_user.id
    ).first_or_404()

    return render_template(
        "main/assignment_detail.html",
        assignment=assignment
    )



# Edit assignment
@main.route("/edit-assignment/<int:assignment_id>", methods=["GET", "POST"])
@login_required
def edit_assignment(assignment_id):

    assignment = Assignment.query.filter_by(
        id=assignment_id,
        user_id=current_user.id
    ).first_or_404()

    form = AssignmentForm(obj=assignment)

    if form.validate_on_submit():

        assignment.title = form.title.data
        assignment.course = form.course.data
        assignment.description = form.description.data
        assignment.due_date = form.due_date.data
        assignment.status = form.status.data

        db.session.commit()

        flash("Assignment updated successfully.", "success")

        return redirect(url_for("main.homepage"))

    return render_template(
        "main/edit_assignment.html",
        form=form,
        assignment=assignment
    )


# Delete assignment
@main.route("/delete-assignment/<int:assignment_id>", methods=["POST"])
@login_required
def delete_assignment(assignment_id):

    assignment = Assignment.query.filter_by(
        id=assignment_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(assignment)
    db.session.commit()

    flash("Assignment deleted successfully.", "success")

    return redirect(url_for("main.homepage"))
