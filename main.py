from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_bootstrap import Bootstrap5

from datetime import date

from forms import TaskForm

app = Flask(__name__)
db = SQLAlchemy()
bootstrap = Bootstrap5(app)
# Create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task-manager.db"
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
# Initialise the app with the extension
db.init_app(app)


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    is_done = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.String)
    # create FK
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))
    # create reference btw tables
    project = relationship(argument="Project", back_populates="tasks")


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    tasks = relationship(argument="Task", back_populates="project")


# with app.app_context():
#     db.create_all()

# Add new tasks and projects
p1 = Project(
    name="Start project"
)

p2 = Project(
    name="School project"
)

t1 = Task(
    name="Go to supermarket",
    date="07/11/2023",
    project=p1
)
t2 = Task(
    name="Clean room",
    date="08/11/2023",
    project=p1
)
t3 = Task(
    name="Finish the project",
    date="10/11/2023",
    project=p2
)

# db.session.add(p1)
# db.session.add(p2)
# db.session.add(t1)
# db.session.add(t2)
# db.session.add(t3)
# db.session.commit()


@app.route("/")
def home():
    today = date.today().strftime("%d.%m.%Y")
    tasks = db.session.execute(db.select(Task)).scalars().all()
    today_tasks = [task for task in tasks if task.date == today]
    return render_template("index.html", all_tasks=today_tasks)


@app.route("/future-tasks/")
def get_future_tasks():
    return render_template("future_tasks.html")


@app.route("/projects/")
def get_projects():
    # TODO: fix a problem with not showing all tasks in project section
    projects = db.session.execute(db.select(Project).order_by("id")).scalars().all()
    tasks_by_projects = []

    proj_ids = [proj.id for proj in projects]
    for proj_id in proj_ids:
        task_list = db.session.execute(db.select(Task).where(Task.project_id == proj_id)).scalars().all()
        tasks_by_projects.append(task_list)

    return render_template("projects.html", all_projects=projects, all_tasks=tasks_by_projects)


@app.route("/add-task", methods=["POST", "GET"])
def add_task():
    add_task_form = TaskForm()
    p_id = 3
    if add_task_form.validate_on_submit():
        new_task = Task(
            name=add_task_form.name.data,
            date=add_task_form.date.data.strftime("%d.%m.%Y"),
            project=db.get_or_404(Project, p_id)
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("add-task.html", form=add_task_form)


@app.route("/edit-task/<int:task_id>", methods=["POST", "GET"])
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)
    task_date = date(day=int(task.date.split(".")[0]),
                     month=int(task.date.split(".")[1]),
                     year=int(task.date.split(".")[2]))
    task_form = TaskForm(
        name=task.name,
        date=task_date,
    )

    if task_form.validate_on_submit():
        date_obj = task_form.date.data
        task.name = task_form.name.data
        task.date = date_obj.strftime("%d.%m.%Y")
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit-task.html", form=task_form)


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task_to_delete = db.get_or_404(Task, task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)

