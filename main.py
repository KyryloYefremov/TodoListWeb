from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

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
    value = db.Column(db.Integer, nullable=False, default=0)
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

# with app.app_context():
#     db.session.add(p1)
#     db.session.add(p2)
#     db.session.add(t1)
#     db.session.add(t2)
#     db.session.add(t3)
#     db.session.commit()


@app.route("/")
def home():
    tasks = db.session.execute(db.select(Task)).scalars().all()
    return render_template("index.html", all_tasks=tasks)


@app.route("/future-tasks/")
def get_future_tasks():
    return render_template("future_tasks.html")


@app.route("/projects/")
def get_projects():
    return render_template("projects.html")


if __name__ == '__main__':
    app.run(debug=True)

