from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from forms import TaskForm

app = Flask(__name__)
db = SQLAlchemy()
# Create database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task-manager.db"
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
    tasks = db.session.execute(db.select(Task)).scalars().all()
    return render_template("index.html", all_tasks=tasks)


@app.route("/future-tasks/")
def get_future_tasks():
    return render_template("future_tasks.html")


@app.route("/projects/")
def get_projects():
    projects = db.session.execute(db.select(Project).order_by("id")).scalars().all()
    tasks_by_projects = []

    proj_ids = [proj.id for proj in projects]
    for proj_id in proj_ids:
        task_list = db.session.execute(db.select(Task).where(Task.project_id == proj_id)).scalars().all()
        tasks_by_projects.append(task_list)

    return render_template("projects.html", all_projects=projects, all_tasks=tasks_by_projects)


@app.route("/edit-task/<int:task_id>", methods=["POST", "GET"])
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)
    return render_template("index.html")


@app.route("/delete")
def delete_task():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)

