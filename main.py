from flask import Flask, session, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_bootstrap import Bootstrap5

from datetime import date, datetime

from forms import TaskForm, ProjectForm

# Mode names
TODAY_PAGE = "Today"
FUTURE_TASK_MODE = "Future"
PROJECTS_MODE = "Projects"
TASK_MODE = "Task"


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
    return render_template("index.html", all_tasks=today_tasks, mode=TODAY_PAGE)


@app.route("/future-tasks/")
def get_future_tasks():
    today = datetime.today()
    all_tasks = Task.query.all()
    future_task = [task for task in all_tasks if datetime.strptime(task.date, "%d.%m.%Y") > today]
    return render_template("index.html", all_tasks=future_task, mode=FUTURE_TASK_MODE)


@app.route("/projects/")
def get_projects():
    projects = db.session.execute(db.select(Project).order_by("id")).scalars().all()
    tasks_by_projects = {}

    proj_ids = [proj.id for proj in projects]
    for proj_id in proj_ids:
        task_list = db.session.execute(db.select(Task).where(Task.project_id == proj_id)).scalars().all()
        tasks_by_projects[proj_id] = task_list

    # <tasks_by_projects> looks like
    #    project_id (key): [<Task 1>, <Task 2>, ...] (value),
    # where value is a list of tasks which belongs to current project
    return render_template("projects.html", all_projects=projects, all_tasks=tasks_by_projects)


@app.route("/add-task/<from_page>", methods=["POST", "GET"])
def add_task(from_page):
    add_task_form = TaskForm()
    # Getting all project from db and send them to TaskForm into select field
    all_projects_obj: list[Project] = db.session.execute(db.select(Project).order_by(Project.id)).scalars().all()
    all_projects: list[str] = [proj.name for proj in all_projects_obj]
    add_task_form.set_projects(existing_projects=all_projects)

    if add_task_form.validate_on_submit():
        proj_name = add_task_form.project.data
        # Getting project obj from the database
        proj = db.session.execute(db.select(Project).where(Project.name == proj_name)).scalar()
        new_task = Task(
            name=add_task_form.name.data,
            date=add_task_form.date.data.strftime("%d.%m.%Y"),
            project=proj
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for(from_page))

    return render_template("add.html", form=add_task_form, mode=TASK_MODE)


@app.route("/edit-task/<int:task_id>/<from_page>", methods=["POST", "GET"])
def edit_task(task_id, from_page):
    task = db.get_or_404(Task, task_id)
    task_date = date(day=int(task.date.split(".")[0]),
                     month=int(task.date.split(".")[1]),
                     year=int(task.date.split(".")[2]))
    # Getting all project from db and send them to TaskForm into select field
    all_projects_obj: list[Project] = db.session.execute(db.select(Project).order_by(Project.id)).scalars().all()
    all_projects: list[str] = [proj.name for proj in all_projects_obj]

    edit_task_form = TaskForm(
        name=task.name,
        date=task_date,
    )
    edit_task_form.set_projects(existing_projects=all_projects)

    selected_project = Project.query.filter_by(id=task.project_id).first()
    if selected_project:
        edit_task_form.project.data = selected_project.name

    if edit_task_form.validate_on_submit():
        date_obj = edit_task_form.date.data
        task.name = edit_task_form.name.data
        task.date = date_obj.strftime("%d.%m.%Y")
        db.session.commit()
        return redirect(url_for(from_page))

    return render_template("edit-task.html", form=edit_task_form)


@app.route("/delete/<int:task_id>/<from_page>")
def delete_task(task_id, from_page):
    task_to_delete = db.get_or_404(Task, task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for(from_page))


@app.route("/add-project", methods=["GET", "POST"])
def add_project():
    add_proj_form = ProjectForm()

    if add_proj_form.validate_on_submit():
        new_proj = Project(
            name=add_proj_form.name.data,
        )
        db.session.add(new_proj)
        db.session.commit()
        return redirect(url_for("get_projects"))

    return render_template("add.html", form=add_proj_form, mode=PROJECTS_MODE[:-1])


@app.route('/update_project', methods=['POST'])
def update_project():
    data = request.get_json()
    project_id = int(data.get('projectId'))
    new_name = data.get('newName')

    proj = db.get_or_404(Project, project_id)
    proj.name = new_name
    db.session.commit()

    return jsonify({'newName': new_name})


@app.route('/toggle_task', methods=['POST'])
def toggle_task():
    print("IN")
    data = request.get_json()
    task_id = int(data.get('taskId'))
    is_checked: bool = data.get('isChecked')
    print(task_id)
    print(is_checked)

    # Обновление состояния чекбокса в базе данных (вместо этого используйте ваш механизм базы данных)
    task_obj = db.get_or_404(Task, task_id)
    task_obj.is_done = int(is_checked)
    db.session.commit()

    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)

